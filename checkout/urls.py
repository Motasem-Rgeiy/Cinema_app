from django.urls import path
from . import views
urlpatterns = [
    path('stripe' , views.stripe_transaction , name='stripe'),
    path('stripe/config' , views.stripe_config),
    path('stripe/webhook' , views.stripe_webhook),
    path('confirmation/<ord>' , views.checkout_confirmation)
]
