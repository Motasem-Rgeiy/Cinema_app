/**
 * static/js/stripe.js
 */

document.addEventListener('DOMContentLoaded', async () => {
    // 1. Fetch the Publishable Key from your Django config endpoint
    const configResponse = await fetch('/checkout/stripe/config');
    const configData = await configResponse.json();
    
    const stripe = Stripe(configData.publicKey);
    const elements = stripe.elements();

    // 2. Setup the Card UI
    const cardElement = elements.create('card', {
        style: {
            base: { fontSize: '16px', color: '#32325d' }
        }
    });
    cardElement.mount('#card-element');

    // 3. Handle the "Credit Card" button click
    const triggerBtn = document.getElementById('card-button-trigger');
    const cardSection = document.getElementById('card-input-section');

    triggerBtn.addEventListener('click', () => {
        cardSection.style.display = 'block';
        triggerBtn.parentElement.style.display = 'none'; // Hide the choice button
    });

    // 4. Handle Final Submission
    const form = document.getElementById('payment-form');
    const submitBtn = document.getElementById('submit-button');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        submitBtn.disabled = true;
        submitBtn.textContent = "Processing...";

        try {
            // A. Request a Client Secret from your Django view
           
            const response = await fetch('/checkout/stripe', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({
                    email: document.getElementById('email').value,
                    first_name: document.getElementById('first_name').value,
                    last_name: document.getElementById('last_name').value,
                    // You can add more data here like total or ticket IDs
                })
            });

            const { client_secret , transaction_id } = await response.json();

            // B. Confirm the payment with Stripe
            const result = await stripe.confirmCardPayment(client_secret, {
                payment_method: {
                    card: cardElement,
                    billing_details: {
                        name: `${document.getElementById('first_name').value} ${document.getElementById('last_name').value}`,
                        email: document.getElementById('email').value
                    }
                }
            });

            if (result.error) {
                // Show error to customer
                document.getElementById('card-errors').textContent = result.error.message;
                submitBtn.disabled = false;
                submitBtn.textContent = "Pay Now";
            } else {
                // Payment success!
                if (result.paymentIntent.status === 'succeeded') {
                    // Redirect to a success page or show a message
                    window.location.href = '/checkout/confirmation'+'/'+String(transaction_id); 
                }
            }
        } catch (err) {
            console.error(err);
            submitBtn.disabled = false;
            submitBtn.textContent = "Pay Now";
        }
    });
});