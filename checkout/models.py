from django.db import models


# Create your models here.

class TransactionStatus(models.IntegerChoices):
    PENDING = 1 , 'pending'
    COMPLETED = 2 , 'completed'

class PaymentMethods(models.IntegerChoices):
    STRIPE = 1 , 'Stripe'

class Transaction(models.Model):
    customer = models.JSONField(default=dict)
    amount = models.FloatField()
    status = models.IntegerField(choices=TransactionStatus.choices , default=TransactionStatus.PENDING)
    items = models.JSONField(default=dict)
    user = models.CharField(max_length=50)
    payment_method = models.IntegerField(choices=PaymentMethods.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    @property
    def customer_name(self):
        return f"{self.customer['first_name']} {self.customer['last_name']}"
    
    @property
    def customer_email(self):
        return f'{self.customer['email']}'


