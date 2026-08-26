from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from apps.orders.models import Order
from apps.payments.models import MpesaPaymentLog, PaymentTransaction

class PaymentWorkflowTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            first_name="Kevin",
            last_name="Mutua",
            phone="254719160398",
            subtotal=Decimal("5000.00"),
            total_amount=Decimal("5200.00")
        )

    def test_mpesa_stk_initiation_and_simulation(self):
        # 1. Initiate STK Push
        response = self.client.post(
            reverse('payments:mpesa_stk_push', kwargs={'order_number': self.order.order_number}),
            {'phone': '0719160398'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        checkout_id = data['checkout_request_id']

        # 2. Simulate User entering PIN
        sim_response = self.client.post(
            reverse('payments:mpesa_simulate_confirm', kwargs={'checkout_request_id': checkout_id})
        )
        self.assertEqual(sim_response.status_code, 200)
        sim_data = sim_response.json()
        self.assertTrue(sim_data['success'])

        # 3. Verify Order updated
        self.order.refresh_from_db()
        self.assertEqual(self.order.payment_status, 'completed')
        self.assertEqual(self.order.status, 'confirmed')
        self.assertTrue(PaymentTransaction.objects.filter(order=self.order, status='successful').exists())
