from .mpesa import MpesaGateway
from .base import BasePaymentGateway
from apps.payments.models import PaymentTransaction


class CashOnDeliveryGateway(BasePaymentGateway):
    def initiate_payment(self, order, request=None, **kwargs):
        order.payment_status = 'pending'
        order.payment_method = 'cash_on_delivery'
        order.status = 'confirmed'
        order.save()
        return {
            'success': True,
            'redirect_to_confirmation': True,
            'message': 'Order confirmed with Pay on Delivery. Our dispatch team will contact you!'
        }


class CardPaymentGateway(BasePaymentGateway):
    def initiate_payment(self, order, request=None, **kwargs):
        # Card processing stub (Ready for Pesapal / Stripe / DPO Kenya)
        return {
            'success': True,
            'message': 'Card payment portal initialized.'
        }


def get_payment_gateway(method_name):
    gateways = {
        'mpesa': MpesaGateway(),
        'cash_on_delivery': CashOnDeliveryGateway(),
        'card': CardPaymentGateway(),
        'manual_transfer': CashOnDeliveryGateway(),
    }
    return gateways.get(method_name, MpesaGateway())
