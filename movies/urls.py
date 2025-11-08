from django.urls import path
from . import views

urlpatterns = [
    # Public URLs
    path('', views.home_view, name='home'),
    path('movies/', views.movie_list_view, name='movie_list'),
    path('movies/<int:movie_id>/', views.movie_detail_view, name='movie_detail'),
    
    # User URLs (Authenticated)
    path('movies/<int:movie_id>/book/', views.book_movie_view, name='book_movie'),
    path('movies/<int:movie_id>/review/', views.review_movie_view, name='review_movie'),
    
    # Admin URLs (Changed from /admin/ to /dashboard/)
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/profile/', views.admin_profile, name='admin_profile'),
    
    # Admin - Movies
    path('dashboard/movies/', views.manage_movies, name='manage_movies'),
    path('dashboard/movies/create/', views.create_movie, name='create_movie'),
    path('dashboard/movies/<int:movie_id>/edit/', views.edit_movie, name='edit_movie'),
    path('dashboard/movies/<int:movie_id>/delete/', views.delete_movie, name='delete_movie'),
    
    # Admin - Genres
    path('dashboard/genres/', views.manage_genres, name='manage_genres'),
    path('dashboard/genres/create/', views.create_genre, name='create_genre'),
    path('dashboard/genres/<int:genre_id>/edit/', views.edit_genre, name='edit_genre'),
    path('dashboard/genres/<int:genre_id>/delete/', views.delete_genre, name='delete_genre'),
    
    # Admin - Bookings
    path('dashboard/bookings/', views.manage_bookings, name='manage_bookings'),
    path('dashboard/bookings/<int:booking_id>/update/', views.update_booking_status, name='update_booking_status'),
    
    # Admin - Reviews
    path('dashboard/reviews/', views.manage_reviews, name='manage_reviews'),
    path('dashboard/reviews/<int:review_id>/approve/', views.approve_review, name='approve_review'),
    path('dashboard/reviews/<int:review_id>/reject/', views.reject_review, name='reject_review'),
    path('dashboard/reviews/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    
    # Admin - Users
    path('dashboard/users/', views.manage_users, name='manage_users'),
    path('dashboard/users/create/', views.create_account, name='create_account'),
    path('dashboard/users/<int:user_id>/edit/', views.edit_account, name='edit_account'),
    path('dashboard/users/<int:user_id>/delete/', views.delete_account, name='delete_account'),
    
    # Admin - Settings
    path('dashboard/settings/', views.admin_settings, name='admin_settings'),
]
