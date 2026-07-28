from django.shortcuts import render , redirect
from django.http import HttpResponse , JsonResponse
from checkout.models import Transaction , PaymentMethods , TransactionStatus
from django.conf import settings
import json
from cinema.models import Cart , Ticket , TicketStatus , Order
import stripe
import math
from django.views.decorators.csrf import csrf_exempt
from cinema.helper import ticket_generation_pdf 
from django.template.loader import render_to_string
from django.core.mail import send_mail 

# Create your views here.

def checkout_confirmation(request , ord):
     Cart.objects.filter(user = request.user).delete()
     transaction = Transaction.objects.filter(id=ord).last()
     return render(request , 'confirmation.html' ,{'order':transaction} )


def stripe_config(request):
    return JsonResponse( {'publicKey':settings.STRIPE_PUBLISHABLE_KEY })

def stripe_transaction(request):
    transaction = make_transaction(request , PaymentMethods.STRIPE)
    if not transaction:
        return JsonResponse('Please enter a vaild information' ,status = 400)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount = transaction.amount * 100,
        currency= settings.CURRENCY,
        payment_method_types= ['card'],
        metadata={
            'transaction':transaction.id
        }
    )
    return JsonResponse({''
    'client_secret':intent['client_secret'],
     'transaction_id': transaction.id
                         })




def make_transaction(request , method):
    customer = json.loads(request.body)
    cart = Cart.objects.filter(user=request.user).last()
    tickets = Ticket.objects.filter(id__in=cart.items)
    total = 0
    for ticket in tickets:
        total+=ticket.showtime.price
    
    if total <= 0:
        return None

    return Transaction.objects.create(
        customer = customer,
        items = cart.items,
        amount = math.ceil(total),
        user = request.user,
        payment_method = method,

    )


@csrf_exempt #stripe avoid this security,so we have to do it by our own
def stripe_webhook(request):
    print('stripe webhook')

    payload = request.body #The raw data Stripe sent (the "Letter")

   
    sig_header = request.META['HTTP_STRIPE_SIGNATURE'] #We get a a signature (key) to ensure that this request came from the correct place
    try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
            )
           # If the signature matches my secret, it creates an event.
    except ValueError as e:
         print("Invalid payload")
         return HttpResponse(status=400)
    
    except stripe.error.SignatureVerificationError as e:
          print('Invalid signature')
          return HttpResponse(status=400)
           

    # Handle the event
    if event and event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']  # contains a stripe.PaymentIntent
        print('payment_intent.successed')
        print(payment_intent.metadata) #It returns transaction id, so we can generate an order based on it
        transaction_id = payment_intent.metadata['transaction']
        print(transaction_id  ,'you done')
        make_order(transaction_id)
    else:
        # Unexpected event type
        print('Unhandled event type {}'.format(event['type']))
    
    return HttpResponse(status=200)
    


def make_order(transaction_id):
          transaction = Transaction.objects.filter(id = transaction_id).last()

          tickets = Ticket.objects.filter(pk__in = transaction.items)
          for ticket in tickets:
               ticket.status = TicketStatus.BOOKED
               ticket_generation_pdf(ticket)
               
          transaction.status = TransactionStatus.COMPLETED
          transaction.save()
          order = Order.objects.create(transaction = transaction)
          print(order)
          #Cart.objects.filter(user = request.user).delete() delete in confirmation page that should be created later
          try:
                order_mail(tickets , order)
                print("success")
          except Exception as e:
               print("The email is faild to sent!" ,e)
                       


    

def order_mail(tickets_obj , order_obj):
     html_msg = render_to_string('emails/order.html',
                                 {'tickets':tickets_obj, 'order':order_obj} #order must be modified in email.html
                                       )
    
     send_mail(subject='Order Completed',
               html_message=html_msg,
               message=html_msg,
               from_email='motasem@example.com',
               recipient_list=[order_obj.transaction.customer_email]

               )