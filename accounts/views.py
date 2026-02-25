from django.shortcuts import render
from django.views.generic import CreateView
from accounts.forms import RegisterForm
from django.urls import reverse_lazy
from django.contrib.auth import login
# Create your views here.


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def get_success_url(self):
        login(self.request , self.object)
        return reverse_lazy('event_list')


