from django.contrib import admin
from . import models
from django.db.models import Count

# Register your models here.

@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_per_page = 20


@admin.register(models.Member)
class MemberAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_select_related = ['role']


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_per_page = 20


@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_select_related = ['category']


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    list_per_page = 20


@admin.register(models.Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id' , 'code' , 'status' , 'user' , 'showtime' , 'seat' , 'updated_at']
    list_per_page = 20

    list_select_related = ['showtime',  'user']

    def has_change_permission(self, request, obj = None):
        return False

@admin.register(models.Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ['id' , 'date' , 'start_time' , 'price' , 'seat_row' , 'seat_column' , 'status' , 'movie' , 'location' , 'tickets_count']
    list_per_page = 20
    list_select_related = ['movie' , 'location']

    def has_change_permission(self, request, obj = None):
        if obj is not None:

            if obj.status == models.ShowtimeStatus.RUNNING or obj.status == models.ShowtimeStatus.FINISHED or obj.status == models.ShowtimeStatus.CANCELLED:
                   return False
        return True
    


    def tickets_count(self , obj):
        return obj.tickets_count
    
    def get_queryset(self, request):
        query = super().get_queryset(request)
        query = query.annotate(tickets_count=Count('ticket'))
        return query

 
  

