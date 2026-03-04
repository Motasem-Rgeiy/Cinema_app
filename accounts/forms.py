from django import forms
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm , UserChangeForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    def __init__(self, *args , **kwargs):
        super(LoginForm , self).__init__(*args , **kwargs)
    
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    username = forms.CharField(widget=forms.TextInput())
    email = forms.CharField(widget=forms.TextInput())
    password1 = forms.CharField(
        widget=forms.PasswordInput() , label='Password'
        )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label="Password Confirmation"
        )

    class Meta(UserCreationForm.Meta):
        fields = ('first_name' , 'last_name', 'username' , 'email')

class ProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['first_name' , 'last_name' , 'email']
        widgets = {
            'first_name':forms.TextInput(),
            'last_name':forms.TextInput(),
            'email':forms.EmailInput(),

        }
