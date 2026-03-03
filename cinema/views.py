from django.shortcuts import render , redirect
from django.http import HttpResponse , JsonResponse
from . import models
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import secrets
from .helper import ticket_generation_pdf , convert_to_numeric
from django.template.loader import render_to_string
from django.core.mail import send_mail 
from .templatetags.my_filters import seat_number



# Create your views here.

class EventListView(LoginRequiredMixin,ListView):
    model = models.Movie
    paginate_by = 4
    template_name = 'index.html'

    def get_queryset(self):
         movies = models.Movie.objects.filter(showtime__status=models.ShowtimeStatus.OPEN).select_related('category').distinct()
         return movies
        
        
   
        
         

#Get the required movie and all locations it is shown on to let the user select which location they want
#then get all avaliable showtimes of the selected location

@login_required
def movieDetails(request , mid):
    movie = models.Movie.objects.filter(pk=mid).prefetch_related('members').last()
    if not movie:
        return HttpResponse('<h1>Not Found</h1>')
    locations = []

    showtimes = models.Showtime.objects.filter(movie_id = mid)
 
    locations = models.Location.objects.filter(pk__in=[loc.location_id for loc in showtimes])
 
    
 #   for showtime in showtimes:

     #           location = models.Location.objects.filter(pk=showtime.location_id).last()
      #          if location not in locations:
  #                   locations.append(location)
  
    return render(request , 'book/movie_details.html' , {'movie':movie , 'locations':locations})


@login_required
def member_details(request , id):
     member =  models.Member.objects.filter(pk = id).select_related('role').last()
     if not member:
          return HttpResponse('<h1>Not Found</h1>')
     return render( request, 'member_details.html' , {'member':member})


@login_required
def get_showtimes(request):
    movie_id = request.GET.get('movie_id')
    location_id = request.GET.get('location_id')
    showtimes = models.Showtime.objects.filter(movie_id = movie_id , location = location_id , status = models.ShowtimeStatus.OPEN)
    
    data = []
    for show in showtimes:
        data.append({'id':show.id , 'start_time':show.start_time , 'date':show.date , 'price':show.price})
    return JsonResponse({'showtimes':data})



@login_required
@csrf_exempt
def save_selected_showtime(request):
   
    if not request.session:
        request.session.create()
       
    request.session['selected_showtime_id'] = json.loads(request.body)
    print('Second', request.session['selected_showtime_id'])
  
    
    return JsonResponse({'status': 'success', 'redirect_url': '/select/seat'})



@login_required
@csrf_exempt
def get_seats(request):
     show_id = request.session.get('selected_showtime_id' , '')
     if not show_id:
               return HttpResponse('<h1>Select a showtime first!</h1>')
          
     show_seats = models.ShowSeat.objects.filter(showtime_id = show_id)
     tickets = models.Ticket.objects.filter(showtime_id = show_id) #
          # reserved_seats = [(seat.row , seat.number) for seat in show_seats]
     reserved_seats = [ticket.seat for ticket in tickets if ticket.seat]
          
     if show_id:
          showtime = models.Showtime.objects.filter(pk=show_id).last()
          rows = range(1 , showtime.seat_row + 1)
          columns = range(1 , showtime.seat_column + 1)
     else:
           rows = (1,)
           columns = (1,)
               
          
    
     return render(request , 'seat_selection.html', {'rows':rows,
                                                       'columns':columns ,
                                                       'showtime':showtime , 
                                                       'show_seats':show_seats,
                                                       'reserved_seats': reserved_seats
                                             })



@login_required
def cart(request):
     return render(request , 'cart.html')


@login_required
@csrf_exempt
def cart_add(request):
    if request.method == 'POST':
        if not request.session:
               request.session.create()
        request.session['show_seats'] =  json.loads(request.body)
       
        show_id = request.session['selected_showtime_id']
        del request.session['selected_showtime_id']
        show_seats = convert_to_numeric(request.session['show_seats'])
       
        tickets = []
        for seat in show_seats:
               tickets.append(
                    models.Ticket(showtime_id = show_id , seat = [seat[0] , seat[1]] , user_id = request.user.id , code = secrets.token_urlsafe(8)) #Save row and column of the chair to the ticket
               )
        
        tickets = [ticket.id for ticket in models.Ticket.objects.bulk_create(tickets)]
        
      #  models.ShowSeat.objects.bulk_create(showSeatList)

        cart_model = models.Cart.objects.filter(user = request.user.id).last()
        if cart_model is None:
             cart_model =  models.Cart.objects.create(user_id = request.user.id , items = tickets)
        else:
             cart_model.items.extend(tickets)
             cart_model.save()
        
        return JsonResponse({
             'message':"This ticket has been added successfully",
             'redirect_url':reverse('event_list')
             })   
    return redirect('/')    
 
   
    

#Get the cart by session
#Get the required ticket
#delete the ticket
@login_required
def cart_remove(request , id):
     session = request.session.session_key
     if not session:
          return JsonResponse({})
     cart = models.Cart.objects.get(user = request.user.id)
     models.Ticket.objects.filter(pk=id).delete()
     if id not in cart.items:
          return HttpResponse('<h1>No Found</h1>')
     cart.items.remove(id)
     cart.save()
     

     return JsonResponse({'message':'The ticket has been removed' , 'status': 'ok'})
     
     



def make_order(request):
     if request.method == 'POST':
          email = request.POST['email']
          first_name = request.POST['first_name']
          last_name = request.POST['last_name']
          customer = {
                        'email':email ,
                        'first_name':first_name,
                        'last_name':last_name,
                        }
          
          total = 0
          cart_model = models.Cart.objects.filter(user = request.user).last()
          tickets = models.Ticket.objects.filter(pk__in = cart_model.items)
          for ticket in tickets:
               total+=ticket.showtime.price
               ticket.status = 2
               ticket_generation_pdf(ticket)
               
          
          order = models.Order.objects.create(customer = customer , total = total)
          models.Cart.objects.filter(user = request.user).delete()
          order_mail(tickets , order)
          return render(request , 'confirmation.html' ,{'order':order})
                       

     else:
          credentials = {}
          if request.user.is_authenticated:
               credentials = {
                    'first_name':request.user.first_name,
                    'last_name':request.user.last_name ,
                    'email': request.user.email ,
                    'password': request.user.password,
               }
         
          return render(request , 'payment.html' , {'credentials':credentials})
    

def order_mail(tickets_obj , order_obj):
     html_msg = render_to_string('emails/order.html',
                                 {'tickets':tickets_obj, 'order':order_obj}
                                       )
     
     send_mail(subject='Order Completed',
               html_message=html_msg,
               message=html_msg,
               from_email='motasem@example.com',
               recipient_list=[order_obj.customer['email']]

               )


def userDashboard(request):
     tickets = models.Ticket.objects.filter(user = request.user).select_related('showtime')
 
     
     dash = []
     
     for ticket in tickets:
          if dash:
               is_exist = False
               for j , row in enumerate(dash):
                    if row['show'] == ticket.showtime and row['status'] == ticket.get_status_display():
                         dash[j]['seat'].append(f"{seat_number(ticket.seat[0])}{ticket.seat[1]}")
                         is_exist = True
                         break
                        
               if not is_exist:
                         dash.append(
               {'show':ticket.showtime , 'status':ticket.get_status_display() , 'seat':[f"{seat_number(ticket.seat[0])}{ticket.seat[1]}"], 'updated_at':ticket.updated_at}
                    )
                       
                    
          else:
               dash.append(
               {'show':ticket.showtime , 'status':ticket.get_status_display() , 'seat':[f"{seat_number(ticket.seat[0])}{ticket.seat[1]}"],'updated_at':ticket.updated_at}
                    )
               
     dash = sorted(dash , key = lambda row: row['updated_at'] , reverse=True)
    
     return render(request , 'dasboard.html' , {  'dashboard':dash})




'''maybe used later
 from django.db.models import Avg
 Book.objects.aggregate(Avg("price", default=0))
'''
