from django.contrib import admin
from .models import Genre, Movie, Booking, Review


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'director', 'release_date', 'status', 'ticket_price', 'available_seats', 'rating']
    list_filter = ['status', 'genre', 'release_date']
    search_fields = ['title', 'director', 'cast']
    ordering = ['-release_date']
    list_editable = ['status', 'ticket_price', 'available_seats']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'show_date', 'show_time', 'number_of_seats', 'total_price', 'status', 'booking_date']
    list_filter = ['status', 'show_date', 'booking_date']
    search_fields = ['user__username', 'movie__title']
    ordering = ['-booking_date']
    list_editable = ['status']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'movie__title', 'comment']
    ordering = ['-created_at']
