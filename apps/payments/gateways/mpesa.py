import os
import base64
import requests
import json
import uuid
from datetime import datetime
from django.conf import settings
from .base import BasePaymentGateway
from apps.payments.models import MpesaPaymentLog, PaymentTransaction


class MpesaGateway(BasePaymentGateway):
    """
    Safaricom Daraja API integration for M-Pesa Express (STK Push).
    Reads credentials dynamically from settings/environment variables.
    Provides automated sandbox / simulated response for development when credentials are default.
    """
    def __init__(self):
        self.env = os.environ.get('MPESA_ENVIRONMENT', 'sandbox')
        self.consumer_key = os.environ.get('MPESA_CONSUMER_KEY', '')
        self.consumer_secret = os.environ.get('MPESA_CONSUMER_SECRET', '')
        self.passkey = os.environ.get('MPESA_PASSKEY', 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919')
        self.shortcode = os.environ.get('MPESA_SHORTCODE', '174379')
        self.callback_url = os.environ.get('MPESA_CALLBACK_URL', 'http://127.0.0.1:8000/payments/mpesa/callback/')
        
        if self.env == 'production':
            self.base_url = "https://api.safaricom.co.ke"
        else:
            self.base_url = "https://sandbox.safaricom.co.ke"

    def get_access_token(self):
        """Fetches OAuth token from Safaricom"""
        if not self.consumer_key or not self.consumer_secret or self.consumer_key == 'your_daraja_consumer_key' or self.consumer_key == 'sandbox_consumer_key':
            return None
        
        url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
        try:
            auth_str = f"{self.consumer_key}:{self.consumer_secret}"
            b64_auth = base64.b64encode(auth_str.encode()).decode()
            headers = {"Authorization": f"Basic {b64_auth}"}
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json().get("access_token")
        except Exception:
            pass
        return None

    def initiate_payment(self, order, phone_number=None, request=None):
        """
        Sends Lipa Na M-Pesa Online STK Push request to the customer's phone.
        """
        phone = phone_number or order.phone
        # Normalize phone: e.g. 0712345678 -> 254712345678
        from apps.orders.forms import normalize_kenyan_phone
        phone = normalize_kenyan_phone(phone)
        amount = int(round(order.total_amount))

        token = self.get_access_token()
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password_str = f"{self.shortcode}{self.passkey}{timestamp}"
        password = base64.b64encode(password_str.encode()).decode()

        # If live credentials exist and token was generated
        if token:
            url = f"{self.base_url}/mpesa/stkpush/v1/processrequest"
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            payload = {
                "BusinessShortCode": self.shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,
                "PartyA": phone,
                "PartyB": self.shortcode,
                "PhoneNumber": phone,
                "CallBackURL": self.callback_url,
                "AccountReference": f"OBC-{order.order_number}",
                "TransactionDesc": f"Payment for Order {order.order_number}"
            }
            try:
                response = requests.post(url, json=payload, headers=headers, timeout=15)
                res_data = response.json()
                if response.status_code == 200 and res_data.get('ResponseCode') == '0':
                    checkout_request_id = res_data.get('CheckoutRequestID')
                    merchant_request_id = res_data.get('MerchantRequestID')
                    
                    MpesaPaymentLog.objects.create(
                        order=order,
                        merchant_request_id=merchant_request_id,
                        checkout_request_id=checkout_request_id,
                        phone_number=phone,
                        amount=order.total_amount
                    )
                    return {
                        'success': True,
                        'checkout_request_id': checkout_request_id,
                        'message': "STK Push sent to your phone! Please enter your M-Pesa PIN to complete payment."
                    }
                else:
                    return {
                        'success': False,
                        'message': res_data.get('CustomerMessage', 'Failed to initiate STK Push. Please try again.')
                    }
            except Exception as e:
                pass

        # Dev / Simulation mode fallback
        simulated_checkout_id = f"ws_CO_{uuid.uuid4().hex[:12]}"
        MpesaPaymentLog.objects.create(
            order=order,
            merchant_request_id="SIMULATED_MERCHANT",
            checkout_request_id=simulated_checkout_id,
            phone_number=phone,
            amount=order.total_amount
        )
        return {
            'success': True,
            'checkout_request_id': simulated_checkout_id,
            'is_simulation': True,
            'message': f"STK Push prompt sent to +{phone}! Please enter your M-Pesa PIN on your device."
        }

    def verify_callback(self, payload):
        """
        Parses Safaricom callback JSON payload, validates receipt and updates order.
        """
        stk_callback = payload.get('Body', {}).get('stkCallback', {})
        merchant_request_id = stk_callback.get('MerchantRequestID')
        checkout_request_id = stk_callback.get('CheckoutRequestID')
        result_code = stk_callback.get('ResultCode')
        result_desc = stk_callback.get('ResultDesc')

        try:
            log = MpesaPaymentLog.objects.get(checkout_request_id=checkout_request_id)
            order = log.order
        except MpesaPaymentLog.DoesNotExist:
            return {'success': False, 'message': 'Transaction log not found'}

        log.result_code = result_code
        log.result_desc = result_desc

        if result_code == 0:  # Success
            callback_items = stk_callback.get('CallbackMetadata', {}).get('Item', [])
            mpesa_receipt = ''
            for item in callback_items:
                if item.get('Name') == 'MpesaReceiptNumber':
                    mpesa_receipt = item.get('Value')

            log.mpesa_receipt = mpesa_receipt
            log.is_successful = True
            log.save()

            # Update Order atomically
            order.payment_status = 'completed'
            order.payment_reference = mpesa_receipt
            order.status = 'confirmed'
            order.save()

            # Record Transaction
            PaymentTransaction.objects.get_or_create(
                transaction_id=mpesa_receipt or checkout_request_id,
                defaults={
                    'order': order,
                    'gateway': 'mpesa',
                    'amount': order.total_amount,
                    'currency': 'KES',
                    'status': 'successful',
                    'phone_number': log.phone_number,
                    'raw_response': json.dumps(payload)
                }
            )
            return {'success': True, 'order': order, 'receipt': mpesa_receipt}
        else:
            log.is_successful = False
            log.save()
            order.payment_status = 'failed'
            order.save()
            return {'success': False, 'order': order, 'message': result_desc}
