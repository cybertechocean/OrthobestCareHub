import json
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages

from apps.orders.models import Order
from .gateways.factory import get_payment_gateway
from .gateways.mpesa import MpesaGateway
from .models import PaymentTransaction, MpesaPaymentLog


class PaymentProcessView(View):
    def get(self, request, order_number):
        order = get_object_or_404(Order, order_number=order_number)
        
        # If already paid or cash on delivery, redirect to confirmation
        if order.payment_status == 'completed' or order.payment_method == 'cash_on_delivery':
            return redirect('orders:order_confirmation', order_number=order.order_number)

        return render(request, "payments/payment_process.html", {
            'order': order,
            'default_phone': order.phone,
        })


class MpesaStkPushAjaxView(View):
    def post(self, request, order_number):
        order = get_object_or_404(Order, order_number=order_number)
        phone = request.POST.get('phone', order.phone).strip()
        
        gateway = MpesaGateway()
        result = gateway.initiate_payment(order=order, phone_number=phone)
        return JsonResponse(result)


class MpesaSimulateConfirmView(View):
    """
    Local simulation helper for developers/testers to simulate customer entering M-Pesa PIN.
    """
    def post(self, request, checkout_request_id):
        log = get_object_or_404(MpesaPaymentLog, checkout_request_id=checkout_request_id)
        order = log.order

        import random
        simulated_receipt = f"QKH{random.randint(1000000, 9999999)}"
        log.result_code = 0
        log.result_desc = "The service request is processed successfully."
        log.mpesa_receipt = simulated_receipt
        log.is_successful = True
        log.save()

        order.payment_status = 'completed'
        order.payment_reference = simulated_receipt
        order.status = 'confirmed'
        order.save()

        PaymentTransaction.objects.get_or_create(
            transaction_id=simulated_receipt,
            defaults={
                'order': order,
                'gateway': 'mpesa',
                'amount': order.total_amount,
                'currency': 'KES',
                'status': 'successful',
                'phone_number': log.phone_number,
                'raw_response': '{"simulation": true}'
            }
        )

        return JsonResponse({
            'success': True,
            'receipt': simulated_receipt,
            'message': 'Simulated M-Pesa payment confirmed successfully!'
        })


class MpesaStatusCheckAjaxView(View):
    def get(self, request, order_number):
        order = get_object_or_404(Order, order_number=order_number)
        return JsonResponse({
            'payment_status': order.payment_status,
            'is_paid': order.payment_status == 'completed',
            'receipt': order.payment_reference,
        })


@method_decorator(csrf_exempt, name='dispatch')
class MpesaCallbackView(View):
    def post(self, request):
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except Exception:
            return JsonResponse({"ResultCode": 1, "ResultDesc": "Invalid JSON"}, status=400)

        gateway = MpesaGateway()
        res = gateway.verify_callback(payload)
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
