from django.urls import path , include
from django.contrib.auth.views import LoginView
from accounts.forms import LoginForm
from accounts.views import RegisterView

urlpatterns = [
    path('login/' , LoginView.as_view(authentication_form = LoginForm) , name='login'),
    path('register/' , RegisterView.as_view() , name='register'),
    path('' , include('django.contrib.auth.urls'))
]
