from django.http import HttpResponse

class WebHookHandler:
    """Handle Stripe webhooks."""
    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        # Handle the webhook request

        return HttpResponse(content=f"unhandled Webhook received: {event['type']}", status=200)

    def handle_payment_intent_succeeded(self, event):
        """Handle the payment succeeded event."""
        # Process the payment succeeded event
        intent = event.data.object
        print(intent)
        
        return HttpResponse(content=f"Webhook received: {event['type']}", status=200)

    def handle_payment_intent_failed(self, event):
        """Handle the payment failed event."""
        # Process the payment failed event
        
        return HttpResponse(content=f"Webhook received: {event['type']}", status=200)