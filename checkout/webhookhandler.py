from django.http import HttpResponse

class StripeWebhookHandler:
    """Handle Stripe webhooks."""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """Handle a generic event from Stripe."""
        return HttpResponse(
            content=f"webhook received: {event['type']}",
            status=200,

        )