from django.shortcuts import render , redirect
from django.http import HttpResponse , JsonResponse
from . import models
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

'''
def event_list(request):
    movies = models.Movie.objects.all()
    paginator = Paginator(movies , 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request , 'index.html' , {'movies':movies , 'page_obj':page_obj})
'''

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
    
    return redirect(request.META.get('HTTP_REFERER', '/'))

def get_seats(request):
     show_id = request.session['selected_showtime_id']
     showtime = models.Showtime.objects.filter(pk=show_id).last()
     rows = range(1 , showtime.seat_row + 1)
     columns = range(1 , showtime.seat_column + 1)
     return render(request , 'seat_selection.html', {'rows':rows , 'columns':columns})




