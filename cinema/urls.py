from django.urls import path
from . import views

urlpatterns = [
    path('' , views.EventListView.as_view() , name='event_list'),
    path('movie/<int:mid>' , views.movieDetails , name='event_details'),
    path('member/<int:id>' , views.member_details , name='member'),
    path('data' , views.save_selected_showtime),
    path('loc/' , views.get_showtimes),
    path('select/seat' , views.get_seats , name = 'select_seat'),
    path('cart/add' , views.cart_add , name = 'cart_add'),
    path('cart/remove/<int:id>', views.cart_remove , name='cart_remove'),
   
 
   
]
