from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Role)
class RoleModel(admin.ModelAdmin):
    list_per_page = 20


@admin.register(models.Member)
class MemberModel(admin.ModelAdmin):
    list_per_page = 20


@admin.register(models.Category)
class CategoryModel(admin.ModelAdmin):
    list_per_page = 20


@admin.register(models.Movie)
class MovieModel(admin.ModelAdmin):
    list_per_page = 20


@admin.register(models.Location)
class LocationModel(admin.ModelAdmin):
    list_per_page = 20


@admin.register(models.Ticket)
class TicketModel(admin.ModelAdmin):
    list_per_page = 20

@admin.register(models.Showtime)
class ShowtimeModel(admin.ModelAdmin):
    list_per_page = 20