class BasePaymentGateway:
    """Abstract Base Class for all payment integrations"""
    
    def initiate_payment(self, order, request=None, **kwargs):
        """
        Initiates a payment workflow.
        Returns a dict e.g. {'success': True, 'redirect_url': '...', 'message': '...'}
        """
        raise NotImplementedError("Payment gateway must implement initiate_payment()")

    def verify_callback(self, payload, **kwargs):
        """
        Processes webhook/callback from payment provider.
        Returns a dict e.g. {'success': True, 'transaction_id': '...', 'order_number': '...'}
        """
        raise NotImplementedError("Payment gateway must implement verify_callback()")
