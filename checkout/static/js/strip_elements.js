

const stripElements = document.getElementById('id_stripe_public_key').textContent.slice(1, -1);
const clientSecret = document.getElementById('id_client_secret').textContent.slice(1, -1);
const stripe = Stripe(stripElements);
const elements = stripe.elements();

const cardElement = elements.create('card');

cardElement.mount('#card-element');

cardElement.on('change', function(event) {
  const displayError = document.getElementById('card-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
});

// Handle form submission
// This function is called when the form is submitted

const form = document.getElementById('payment-form');


form.addEventListener('submit', function(event) {
  event.preventDefault();
  cardElement.update({ disabled: true });
  document.getElementById('submit-button').disabled = true;
  stripe.confirmCardPayment(clientSecret, {
    payment_method: {
      card: cardElement,
      billing_details: {
        name: document.getElementById('id_name').value,
        email: document.getElementById('id_email').value
      }
    }
  }).then(function(result) {
    if (result.error) {
      const displayError = document.getElementById('card-errors');
      displayError.textContent = result.error.message;
      cardElement.update({ disabled: false });
      document.getElementById('submit-button').disabled = false;
    } else {
      if (result.paymentIntent.status === 'succeeded') {
        form.submit();
      }
    }
  });
});
