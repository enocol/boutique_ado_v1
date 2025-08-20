

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
const submitBtn = document.getElementById('submit-button');
const errorBox  = document.getElementById('card-errors');


// form.addEventListener('submit', function(event) {
//   event.preventDefault();
//   cardElement.update({ disabled: true });
//   document.getElementById('submit-button').disabled = true;
//   let saveInfo = document.getElementById('id_save_info').checked
//   let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
//   let postData = {
//     'csrfmiddlewaretoken': csrfToken,
//     'client_secret': clientSecret,
//     'save_info': saveInfo,
//   };
//   console.log('Post data i am here:', postData);
//   let url = '/cache_checkout_data/';
//   fetch(url, {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json',
//       'X-CSRFToken': csrfToken,
//     },
//     body: JSON.stringify(postData),
//   }).then(function(response) {
//     if (!response.ok) {
//       throw new Error('Network response was not ok');
//     }
//     return response.json();
//   }).catch(function(error) {
//     const displayError = document.getElementById('card-errors');
//     displayError.textContent = error.message;
//     cardElement.update({ disabled: false });
//     document.getElementById('submit-button').disabled = false;
//   });
//   // Confirm the card payment
//   console.log( 'i am here in confirm card payment');
//   stripe.confirmCardPayment(clientSecret, {
//     payment_method: {
//       card: cardElement,
//       billing_details: {
//         name: form.elements['full_name'].value,
//         phone: form.elements['phone_number'].value,
//         email: form.elements['email'].value,
//         address: {
//           line1: form.elements['address_line_1'].value,
//           line2: form.elements['address_line_2'].value,
//           city: form.elements['city'].value,
//           state: form.elements['state'].value,
//           postal_code: form.elements['postal_code'].value,
//           country: form.elements['country'].value
//         },
        

//       }
//     },
//     shipping: {
//       name: form.elements['full_name'].value,
//       email: form.elements['email'].value,
//       phone: form.elements['phone_number'].value,
//       address: {
//         line1: form.elements['address_line_1'].value,
//         line2: form.elements['address_line_2'].value,
//         city: form.elements['city'].value,
//         state: form.elements['state'].value,
//         postal_code: form.elements['postal_code'].value,
//         country: form.elements['country'].value
//       }
//     }
//   }).then(function(result) {
//     if (result.error) {
//       const displayError = document.getElementById('card-errors');
//       displayError.textContent = result.error.message;
//       cardElement.update({ disabled: false });
//       document.getElementById('submit-button').disabled = false;
//     } else {
//       if (result.paymentIntent.status === 'succeeded') {
//         form.submit();
//       }
//     }
//   });
// });

function setUIDisabled(disabled) {
  cardElement.update({ disabled });
  if (submitBtn) submitBtn.disabled = disabled;
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  setUIDisabled(true);
  errorBox.textContent = '';

  // Collect values (ensure inputs exist in your form)
  const name        = form.elements['full_name']?.value || '';
  const email       = form.elements['email']?.value || '';
  const phone       = form.elements['phone_number']?.value || '';
  const line1       = form.elements['address_line_1']?.value || '';
  const line2       = form.elements['address_line_2']?.value || '';
  const city        = form.elements['city']?.value || '';
  const state       = form.elements['state']?.value || '';
  const postal_code = form.elements['postal_code']?.value || '';
  const countryRaw  = form.elements['country']?.value || '';
  const country     = countryRaw.toString().trim().toUpperCase(); // ISO 2 letters (e.g., GB)
  const saveInfo    = document.getElementById('id_save_info')?.checked || false;

  // 1) Cache checkout data on your server BEFORE confirming payment
  try {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
   

    const resp = await fetch('cache_checkout_data/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({
        save_info: saveInfo,
        client_secret: clientSecret,
      }),
    });

    if (!resp.ok) {
      let msg = 'Could not cache checkout data.';
      try {
        const data = await resp.json();
        if (data?.error) msg = data.error;
      } catch {}
      throw new Error(msg);
    }
  } catch (err) {
    errorBox.textContent = err.message || 'Network error while caching checkout data.';
    setUIDisabled(false);
    return;
  }


  // 2) Confirm the card payment
  try {
    
    const result = await stripe.confirmCardPayment(clientSecret, {
      
      payment_method: {
        card: cardElement,
        // Billing follows Stripe schema: no `email` here
        billing_details: {
          name,
          email,
          phone,
          address: {
            line1,
            line2,
            city,
            state,
            postal_code,
            country,
          },
        },
      },
      // Shipping follows Stripe schema: no `email` here
      shipping: {
        name,
        phone,
        address: {
          line1,
          line2,
          city,
          state,
          postal_code,
          country,
        },
      },
      
    });
    

    if (result.error) {
      errorBox.textContent = result.error.message || 'Payment failed.';
      setUIDisabled(false);
      return;
    }


    if (result.paymentIntent?.status === 'succeeded') {
      console.log('Payment succeeded, submitting form');
        
      form.submit(); // let server finalize the order
      
    
    } else {
      errorBox.textContent = 'Payment could not be completed.';
      setUIDisabled(false);
    }
    console.log('Payment succeeded');
  } catch (err) {
    errorBox.textContent = err.message || 'Unexpected error during payment.';
    setUIDisabled(false);
  }
});
