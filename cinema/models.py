from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
# Create your models here.



class Role(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name



class Member(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    image = models.ImageField()
    birthdate = models.DateField(null=True)
    role = models.ForeignKey(Role , on_delete=models.PROTECT)

    def __str__(self):
        return self.name



class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name



class Movie(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    run_time = models.DurationField()
    image = models.ImageField(null=True)
    category = models.ForeignKey(Category , on_delete=models.PROTECT)
    members = models.ManyToManyField(Member)

    def __str__(self):
        return self.name

class Location(models.Model):
    city = models.CharField(max_length=200)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.city



class Showtime(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    price = models.FloatField()
    seat_row = models.IntegerField(null=True)
    seat_column = models.IntegerField(null=True)
    movie = models.ForeignKey(Movie , on_delete=models.CASCADE , null=True)
    location = models.ForeignKey(Location , on_delete=models.PROTECT)

    def __str__(self):
        return str(self.start_time)



#To check for available chairs
class ShowSeat(models.Model):
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    row = models.IntegerField()
    number = models.IntegerField()


class TicketStatus(models.IntegerChoices):
    RESERVED = 1 , 'reserved'
    BOOKED = 2 , 'booked'

class Ticket(models.Model):
    code = models.CharField(max_length=20 , unique=True , null=True)
    status = models.IntegerField(choices=TicketStatus.choices , default=TicketStatus.RESERVED)
    pdf_file = models.FileField(blank=True , null=True)
    user = models.ForeignKey(User ,on_delete=models.CASCADE, null=True)
    showtime = models.ForeignKey(Showtime , on_delete=models.CASCADE)
    seat = models.JSONField(default=dict)




class Order(models.Model):
    total = models.FloatField()
    customer = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True , null=True)
    updated_at = models.DateTimeField(auto_now=True , null=True)

    @property
    def customer_name(self):
        return f"{self.customer['first_name']} {self.customer['last_name']}"




class Cart(models.Model):
   # session = models.ForeignKey(Session , on_delete=models.CASCADE)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    items = models.JSONField(default=dict)