from django.shortcuts import render
from django.views.generic import CreateView , UpdateView
from accounts.forms import RegisterForm , ProfileForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def get_success_url(self):
        login(self.request , self.object)
        return reverse_lazy('event_list')
    
class ProfileView(LoginRequiredMixin , UpdateView):
    form_class = ProfileForm
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset = None):
        return self.request.user


