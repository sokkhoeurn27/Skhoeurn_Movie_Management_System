from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Genre(models.Model):
    """
    Genre model for movie categories
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'genres'
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Movie(models.Model):
    """
    Movie model for storing movie information
    """
    STATUS_CHOICES = (
        ('now_showing', 'Now Showing'),
        ('coming_soon', 'Coming Soon'),
        ('archived', 'Archived'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, related_name='movies')
    duration = models.IntegerField(help_text='Duration in minutes')
    release_date = models.DateField()
    director = models.CharField(max_length=100)
    cast = models.TextField(help_text='Comma-separated list of actors')
    poster = models.ImageField(upload_to='movies/posters/', blank=True, null=True)
    trailer_url = models.URLField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, 
                                  validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='now_showing')
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    available_seats = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'movies'
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
        ordering = ['-release_date']
    
    def __str__(self):
        return f"{self.title} ({self.release_date.year})"
    
    def is_available(self):
        return self.available_seats > 0 and self.status == 'now_showing'
    
    def get_trailer_embed_url(self):
        """Convert YouTube URL to embed URL"""
        if not self.trailer_url:
            return ''
        
        url = self.trailer_url
        video_id = None
        
        # Extract video ID from different YouTube URL formats
        if 'youtu.be' in url:
            # https://youtu.be/VIDEO_ID
            video_id = url.split('youtu.be/')[-1].split('?')[0].split('&')[0]
        elif 'youtube.com/watch' in url:
            # https://www.youtube.com/watch?v=VIDEO_ID
            if '?v=' in url:
                video_id = url.split('?v=')[-1].split('&')[0]
            elif '&v=' in url:
                video_id = url.split('&v=')[-1].split('&')[0]
        elif 'youtube.com/embed' in url:
            # https://www.youtube.com/embed/VIDEO_ID
            video_id = url.split('embed/')[-1].split('?')[0]
        
        if video_id:
            return f'https://www.youtube.com/embed/{video_id}'
        
        return url
    
    def get_youtube_video_id(self):
        """Extract just the video ID from YouTube URL"""
        if not self.trailer_url:
            return ''
        
        url = self.trailer_url
        
        # Extract video ID from different YouTube URL formats
        if 'youtu.be' in url:
            return url.split('youtu.be/')[-1].split('?')[0].split('&')[0]
        elif 'youtube.com/watch' in url:
            if '?v=' in url:
                return url.split('?v=')[-1].split('&')[0]
            elif '&v=' in url:
                return url.split('&v=')[-1].split('&')[0]
        elif 'youtube.com/embed' in url:
            return url.split('embed/')[-1].split('?')[0]
        
        return ''
    
    def average_rating(self):
        """Calculate average rating from user reviews"""
        reviews = self.reviews.filter(is_approved=True)
        if reviews.exists():
            return round(reviews.aggregate(models.Avg('rating'))['rating__avg'], 1)
        return 0.0
    
    def update_rating(self):
        """Update the rating field based on approved reviews"""
        self.rating = self.average_rating()
        self.save(update_fields=['rating', 'updated_at'])
    
    def get_review_count(self):
        """Get the number of approved reviews"""
        return self.reviews.filter(is_approved=True).count()


class Booking(models.Model):
    """
    Booking model for movie ticket bookings
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    show_date = models.DateField()
    show_time = models.TimeField()
    number_of_seats = models.IntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'bookings'
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-booking_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.movie.title} ({self.show_date})"
    
    def calculate_total_price(self):
        return self.movie.ticket_price * self.number_of_seats


class Review(models.Model):
    """
    Review model for movie reviews
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reviews'
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']
        unique_together = ['user', 'movie']  # One review per user per movie
    
    def __str__(self):
        return f"{self.user.username} - {self.movie.title} ({self.rating}/5)"
    
    def save(self, *args, **kwargs):
        """Override save to update movie rating after saving review"""
        super().save(*args, **kwargs)
        # Update movie rating after review is saved
        self.movie.update_rating()
    
    def delete(self, *args, **kwargs):
        """Override delete to update movie rating after deleting review"""
        movie = self.movie
        super().delete(*args, **kwargs)
        # Update movie rating after review is deleted
        movie.update_rating()


class SiteSetting(models.Model):
    """
    Site settings model for storing system configuration
    """
    site_name = models.CharField(max_length=200, default='Movie Management System')
    site_email = models.EmailField(default='admin@moviemanagement.com')
    items_per_page = models.IntegerField(default=10, validators=[MinValueValidator(5), MaxValueValidator(100)])
    site_logo = models.ImageField(upload_to='site/', blank=True, null=True)
    enable_review = models.BooleanField(default=True)
    require_approval = models.BooleanField(default=False)
    enable_notification = models.BooleanField(default=True)
    maintenance_mode = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'site_settings'
        verbose_name = 'Site Setting'
        verbose_name_plural = 'Site Settings'
    
    def __str__(self):
        return f"Settings - {self.site_name}"
    
    @classmethod
    def get_settings(cls):
        """Get or create site settings (singleton pattern)"""
        settings, created = cls.objects.get_or_create(id=1)
        return settings
