from django.urls import path
from . import views

urlpatterns = [
    path('' , views.EventListView.as_view() , name='event_list'),
    path('movie/<int:mid>' , views.movieDetails , name='event_details'),
    path('data' , views.save_selected_showtime),
    path('loc/' , views.get_showtimes),
    path('select/seat' , views.get_seats , name = 'select_seat')
 
   
]
