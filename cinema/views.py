from django.shortcuts import render , redirect
from django.http import HttpResponse , JsonResponse
from . import models
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

class EventListView(ListView):
    model = models.Movie
    paginate_by = 4
    template_name = 'index.html'

#Get the required movie and all locations it is shown on to let the user select which location they want
#then get all avaliable showtimes of the selected location
def movieDetails(request , mid):
    movie = models.Movie.objects.filter(pk=mid).prefetch_related('members').last()
    if not movie:
        return
    locations = []
    showtimes = models.Showtime.objects.filter(movie_id = mid)
    for showtime in showtimes:

                location = models.Location.objects.filter(pk=showtime.location_id).last()
                if location not in locations:
                     locations.append(location)
  
    return render(request , 'book/movie_details.html' , {'movie':movie , 'locations':locations})

def get_showtimes(request):
    movie_id = request.GET.get('movie_id')
    location_id = request.GET.get('location_id')
    showtimes = models.Showtime.objects.filter(movie_id = movie_id , location = location_id)
    
    data = []
    for show in showtimes:
        data.append({'id':show.id , 'start_time':show.start_time})
    return JsonResponse({'showtimes':data})

@csrf_exempt
def save_selected_showtime(request):
    if not request.session:
        request.session.create()
    request.session['selected_showtime_id'] = json.loads(request.body)
    print(request.session['selected_showtime_id'] )
    
    return redirect(request.META.get('HTTP_REFERER', '/'))



def get_seats(request):
     show_id = request.session.get('selected_showtime_id' , '')
     show_seats = models.ShowSeat.objects.filter(showtime_id = show_id)
    # reserved_row_seats = [seat.row for seat in show_seats]
    # reserved_number_seats = [seat.number for seat in show_seats]
    # print(reserved_row_seats)
    # print(reserved_number_seats)
     reserved_seats = [(seat.row , seat.number) for seat in show_seats]
     print(reserved_seats)
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


#showtime
#the number and names of selected seats
#create tickets with default status
#create a cart has the required tickets and a session


@csrf_exempt
def cart_add(request):
     if request.method == 'POST':
          if not request.session:
               request.session.create()
          request.session['show_seats'] =  json.loads(request.body)
          show_id = request.session['selected_showtime_id']
          show_seats = convert_to_numeric(request.session['show_seats'])
          showSeatList = []
          for seat in show_seats:
               showSeatList.append(
                    models.ShowSeat(row = seat[0] , number = seat[1] , showtime_id = show_id)
                    )
               
          models.ShowSeat.objects.bulk_create(showSeatList , update_conflicts=True)
               

          return redirect(request.META.get('HTTP_REFERER' , '/'))
         
     return render(request , 'cart.html')

def convert_to_numeric(show_seats):
     rows = [ele[0] for ele in show_seats]
     print(rows)
     new = []
     for seat in show_seats:
          row = ord(seat[0]) -  65  + 1
          new.append((row , int(seat[1])))
     return new