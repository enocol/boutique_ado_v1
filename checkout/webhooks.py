from checkout.stripwebHookhandler import WebHookHandler
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST 
import stripe

from django.conf import settings


# Using Django
# Replace this endpoint secret with your unique endpoint secret key
# If you're testing with the CLI, run 'stripe listen' to find the secret key
# If you defined your endpoint using the API or the Dashboard, check your webhook settings for your endpoint secret: https://dashboard.stripe.com/webhooks
endpoint_secret = 'whsec_...'

@csrf_exempt
@require_POST
def webhook(request):
  
#   setup stripe with your secret key
  stripe.api_key = settings.STRIPE_SECRET_KEY
  wh_secret = settings.STRIPE_WH_SECRET.strip()  # Ensure no leading/trailing spaces

  payload = request.body
  event = None
  sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, wh_secret
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)

  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)
  except Exception as e:
    # Handle other exceptions
    return HttpResponse(content=str(e), status=400)


  # Handle the event
  handler = WebHookHandler(request)

  event_map = {
      'payment_intent.payment_succeeded': handler.handle_payment_intent_succeeded,
      'payment_intent.payment_failed': handler.handle_payment_intent_failed,
  }

  event_type = event['type']

  event_handler = event_map.get(event_type, handler.handle_event)

 # Return a response to acknowledge receipt of the event
  response = event_handler(event)
  if response:
        return response