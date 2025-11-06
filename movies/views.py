from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from .models import Movie, Genre, Booking, Review
from .forms import MovieForm, GenreForm, BookingForm, ReviewForm, BookingStatusForm, MovieSearchForm
from accounts.models import Account
from accounts.forms import AdminCreateAccountForm, AdminEditAccountForm


# ==================== PUBLIC VIEWS ====================

def home_view(request):
    """
    Home page - show featured movies
    """
    now_showing = Movie.objects.filter(status='now_showing').order_by('-created_at')[:6]
    coming_soon = Movie.objects.filter(status='coming_soon').order_by('release_date')[:3]
    genres = Genre.objects.all()
    
    context = {
        'now_showing': now_showing,
        'coming_soon': coming_soon,
        'genres': genres,
    }
    
    return render(request, 'User/home.html', context)


def movie_list_view(request):
    """
    List all movies with search and filter
    """
    movies = Movie.objects.filter(status='now_showing')
    genres = Genre.objects.all()
    
    form = MovieSearchForm(request.GET)
    
    if form.is_valid():
        # Search
        search_query = form.cleaned_data.get('search', '')
        if search_query:
            movies = movies.filter(
                Q(title__icontains=search_query) | 
                Q(director__icontains=search_query) |
                Q(cast__icontains=search_query)
            )
        
        # Filter by genre
        genre = form.cleaned_data.get('genre')
        if genre:
            movies = movies.filter(genre=genre)
    
    context = {
        'movies': movies,
        'form': form,
    }
    
    return render(request, 'User/movie_list.html', context)


def movie_detail_view(request, movie_id):
    """
    Movie detail page with reviews
    """
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = movie.reviews.all().order_by('-created_at')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    context = {
        'movie': movie,
        'reviews': reviews,
        'avg_rating': avg_rating,
    }
    
    return render(request, 'User/movie_detail.html', context)


# ==================== USER VIEWS (Authenticated) ====================

@login_required
def book_movie_view(request, movie_id):
    """
    Book movie tickets
    """
    movie = get_object_or_404(Movie, id=movie_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.movie = movie
            
            # Validation
            if booking.number_of_seats > movie.available_seats:
                messages.error(request, 'Not enough seats available!')
                return render(request, 'User/book_movie.html', {'movie': movie, 'form': form})
            
            # Calculate total price
            booking.total_price = movie.ticket_price * booking.number_of_seats
            booking.status = 'confirmed'
            booking.save()
            
            # Update available seats
            movie.available_seats -= booking.number_of_seats
            movie.save()
            
            messages.success(request, 'Booking confirmed successfully!')
            return redirect('profile')
    else:
        form = BookingForm()
    
    context = {
        'movie': movie,
        'form': form,
    }
    
    return render(request, 'User/book_movie.html', context)


@login_required
def review_movie_view(request, movie_id):
    """
    Add or edit movie review
    """
    movie = get_object_or_404(Movie, id=movie_id)
    
    # Check if user already reviewed this movie
    existing_review = Review.objects.filter(user=request.user, movie=movie).first()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            
            if existing_review:
                messages.success(request, 'Review updated successfully!')
            else:
                messages.success(request, 'Review added successfully!')
            
            return redirect('movie_detail', movie_id=movie_id)
    else:
        form = ReviewForm(instance=existing_review)
    
    context = {
        'movie': movie,
        'form': form,
        'existing_review': existing_review,
    }
    
    return render(request, 'User/review_movie.html', context)


# ==================== ADMIN VIEWS ====================

@login_required
def admin_dashboard(request):
    """
    Admin dashboard - only accessible to admin users
    """
    if not request.user.is_admin():
        messages.error(request, 'Access denied! Admin only.')
        return redirect('home')
    
    from django.utils import timezone
    from datetime import timedelta
    import json
    
    # Basic Statistics
    total_movies = Movie.objects.count()
    total_users = Account.objects.filter(role='user').count()
    total_bookings = Booking.objects.count()
    total_reviews = Review.objects.count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    
    # Monthly Growth Calculations
    now = timezone.now()
    last_month = now - timedelta(days=30)
    
    # Movies growth
    movies_this_month = Movie.objects.filter(created_at__gte=last_month).count()
    movies_last_month = Movie.objects.filter(
        created_at__gte=last_month - timedelta(days=30),
        created_at__lt=last_month
    ).count()
    movies_growth = ((movies_this_month - movies_last_month) / movies_last_month * 100) if movies_last_month > 0 else 0
    
    # Users growth
    users_this_month = Account.objects.filter(created_at__gte=last_month, role='user').count()
    users_last_month = Account.objects.filter(
        created_at__gte=last_month - timedelta(days=30),
        created_at__lt=last_month,
        role='user'
    ).count()
    users_growth = ((users_this_month - users_last_month) / users_last_month * 100) if users_last_month > 0 else 0
    
    # Reviews growth
    reviews_this_month = Review.objects.filter(created_at__gte=last_month).count()
    reviews_last_month = Review.objects.filter(
        created_at__gte=last_month - timedelta(days=30),
        created_at__lt=last_month
    ).count()
    reviews_growth = ((reviews_this_month - reviews_last_month) / reviews_last_month * 100) if reviews_last_month > 0 else 0
    
    # Monthly Activity Chart Data (Last 6 months)
    monthly_activity = []
    for i in range(5, -1, -1):
        month_start = now - timedelta(days=30 * i)
        month_end = now - timedelta(days=30 * (i - 1)) if i > 0 else now
        
        bookings_count = Booking.objects.filter(
            booking_date__gte=month_start,
            booking_date__lt=month_end
        ).count()
        
        reviews_count = Review.objects.filter(
            created_at__gte=month_start,
            created_at__lt=month_end
        ).count()
        
        monthly_activity.append({
            'month': month_start.strftime('%b'),
            'bookings': bookings_count,
            'reviews': reviews_count
        })
    
    # Movies by Genres Chart Data
    genres = Genre.objects.all()
    movies_by_genre = []
    for genre in genres:
        count = genre.movies.count()
        if count > 0:
            movies_by_genre.append({
                'genre': genre.name,
                'count': count
            })
    
    # Rating Distribution Chart Data
    rating_distribution = []
    for rating in range(1, 6):
        count = Review.objects.filter(rating=rating).count()
        rating_distribution.append({
            'rating': f'{rating} Star{"s" if rating > 1 else ""}',
            'count': count
        })
    
    # Recent Movies (Last 5)
    recent_movies = Movie.objects.order_by('-created_at')[:5]
    
    # Recent Reviews (Last 5)
    recent_reviews = Review.objects.select_related('movie', 'user').order_by('-created_at')[:5]
    
    # Recent data
    recent_bookings = Booking.objects.all().order_by('-booking_date')[:5]
    
    context = {
        'total_movies': total_movies,
        'total_users': total_users,
        'total_bookings': total_bookings,
        'total_reviews': total_reviews,
        'pending_bookings': pending_bookings,
        'movies_growth': round(movies_growth, 1),
        'users_growth': round(users_growth, 1),
        'reviews_growth': round(reviews_growth, 1),
        'monthly_activity': json.dumps(monthly_activity),
        'movies_by_genre': json.dumps(movies_by_genre),
        'rating_distribution': json.dumps(rating_distribution),
        'recent_movies': recent_movies,
        'recent_reviews': recent_reviews,
        'recent_bookings': recent_bookings,
    }
    
    return render(request, 'Admin/dashboard.html', context)


@login_required
def manage_movies(request):
    """
    Admin - Manage all movies
    """
    if not request.user.is_admin():
        messages.error(request, 'Access denied! Admin only.')
        return redirect('home')
    
    movies = Movie.objects.all().order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        movies = movies.filter(
            Q(title__icontains=search_query) |
            Q(director__icontains=search_query) |
            Q(genre__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    context = {
        'movies': movies,
        'search_query': search_query,
    }
    
    return render(request, 'Admin/manage_movies.html', context)


@login_required
def create_movie(request):
    """
    Admin - Create new movie
    """
    if not request.user.is_admin():
        messages.error(request, 'Access denied! Admin only.')
        return redirect('home')
    
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Movie created successfully!')
            return redirect('manage_movies')
    else:
        form = MovieForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'Admin/create_movie.html', context)


@login_required
def edit_movie(request, movie_id):
    """
    Admin - Edit existing movie
    """
    if not request.user.is_admin():
        messages.error(request, 'Access denied! Admin only.')
        return redirect('home')
    
    movie = get_object_or_404(Movie, id=movie_id)
    
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            messages.success(request, 'Movie updated successfully!')
            return redirect('manage_movies')
    else:
        form = MovieForm(instance=movie)
    
    context = {
        'form': form,
        'movie': movie,
    }
    
    return render(request, 'Admin/edit_movie.html', context)


@login_required
def delete_movie(request, movie_id):
    """
    Admin - Delete movie
    """
    if not request.user.is_admin():
        messages.error(request, 'Access denied! Admin only.')
        return redirect('home')
    
    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    
    messages.success(request, 'Movie deleted successfully!')
    return redirect('manage_movies')


@login_required
def manage_genres(request):
    """
    Admin - Manage genres
    """
    if not request.user.is_admin():
        messages.error(request, 'Access denied! Admin only.')
        return redirect('home')
    
    genres = Genre.objects.all().order_by('name')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        genres = genres.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    context = {
        'genres': genres,
        'search_query': search_query,
    }
    
    return render(request, 'Admin/manage_genres.html', context)


@login_required
def create_genre(request):
    """
    Admin - Create new genre
    """
    if not request.user.is_admin():
        messages.error(request, 'Access denied! Admin only.')
        return redirect('home')
    
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Genre created successfully!')
            return redirect('manage_genres')
    else:
        form = GenreForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'Admin/create_genres.html', context)


@login_required
def edit_genre(request, genre_id):
    """
    Admin - Edit genre
    """
    if not request.user.is_admin():
        messages.error(request, 'Access denied! Admin only.')
        return redirect('home')
    
    genre = get_object_or_404(Genre, id=genre_id)
    
    if request.method == 'POST':
        form = GenreForm(request.POST, instance=genre)
        if form.is_valid():
            form.save()
            messages.success(request, 'Genre updated successfully!')
            return redirect('manage_genres')
    else:
        form = GenreForm(instance=genre)
    
    context = {
        'form': form,
        'genre': genre,
    }
    
    return render(request, 'Admin/edit_genres.html', context)


@login_required
def delete_genre(request, genre_id):
    """
    Admin - Delete genre
    """
    if not request.user.is_admin():
        messages.error(request, 'Access denied! Admin only.')
        return redirect('home')
    
    genre = get_object_or_404(Genre, id=genre_id)
    genre.delete()
    
    messages.success(request, 'Genre deleted successfully!')
    return redirect('manage_genres')


@login_required
def manage_bookings(request):
    """
    Admin - Manage all bookings
    """
    if not request.user.is_admin():
        messages.error(request, 'Access denied! Admin only.')
        return redirect('home')
    
    bookings = Booking.objects.all().order_by('-booking_date')
    
    context = {
        'bookings': bookings,
    }
    
    return render(request, 'Admin/manage_bookings.html', context)


@login_required
def update_booking_status(request, booking_id):
    """
    Admin - Update booking status
    """
    if not request.user.is_admin():
        messages.error(request, 'Access denied! Admin only.')
        return redirect('home')
    
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        form = BookingStatusForm(request.POST, instance=booking)
        if form.is_valid():
            old_status = booking.status
            new_booking = form.save()
            
            # If cancelled, return seats to movie
            if new_booking.status == 'cancelled' and old_status != 'cancelled':
                movie = new_booking.movie
                movie.available_seats += new_booking.number_of_seats
                movie.save()
            
            messages.success(request, 'Booking status updated!')
            return redirect('manage_bookings')
    
    return redirect('manage_bookings')


@login_required
def manage_reviews(request):
    """
    Admin - Manage all reviews
    """
    if not request.user.is_admin():
        messages.error(request, 'Access denied! Admin only.')
        return redirect('home')
    
    reviews = Review.objects.all().order_by('-created_at')
    
    context = {
        'reviews': reviews,
    }
    
    return render(request, 'Admin/manage_reviews.html', context)


@login_required
def delete_review(request, review_id):
    """
    Admin - Delete review
    """
    if not request.user.is_admin():
        messages.error(request, 'Access denied! Admin only.')
        return redirect('home')
    
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    
    messages.success(request, 'Review deleted successfully!')
    return redirect('manage_reviews')


@login_required
def manage_users(request):
    """
    Admin - Manage all users
    """
    if not request.user.is_admin():
        messages.error(request, 'Access denied! Admin only.')
        return redirect('home')
    
    users = Account.objects.all().order_by('-created_at')
    
    context = {
        'users': users,
    }
    
    return render(request, 'Admin/manage_users.html', context)


@login_required
def create_account(request):
    """
    Admin - Create new user account
    """
    if not request.user.is_admin():
        messages.error(request, 'Access denied! Admin only.')
        return redirect('home')
    
    if request.method == 'POST':
        form = AdminCreateAccountForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('manage_users')
    else:
        form = AdminCreateAccountForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'Admin/create_account.html', context)


@login_required
def edit_account(request, user_id):
    """
    Admin - Edit user account
    """
    if not request.user.is_admin():
        messages.error(request, 'Access denied! Admin only.')
        return redirect('home')
    
    user = get_object_or_404(Account, id=user_id)
    
    if request.method == 'POST':
        form = AdminEditAccountForm(request.POST, instance=user)
        if form.is_valid():
            account = form.save(commit=False)
            
            # Update password if provided
            new_password = form.cleaned_data.get('password')
            if new_password:
                account.set_password(new_password)
            
            account.save()
            messages.success(request, 'Account updated successfully!')
            return redirect('manage_users')
    else:
        form = AdminEditAccountForm(instance=user)
    
    context = {
        'form': form,
        'account': user,
    }
    
    return render(request, 'Admin/edit_account.html', context)


@login_required
def delete_account(request, user_id):
    """
    Admin - Delete user account
    """
    if not request.user.is_admin():
        messages.error(request, 'Access denied! Admin only.')
        return redirect('home')
    
    user = get_object_or_404(Account, id=user_id)
    
    if user == request.user:
        messages.error(request, 'You cannot delete your own account!')
        return redirect('manage_users')
    
    user.delete()
    
    messages.success(request, 'Account deleted successfully!')
    return redirect('manage_users')


@login_required
def admin_settings(request):
    """
    Admin - Settings page
    """
    if not request.user.is_admin():
        messages.error(request, 'Access denied! Admin only.')
        return redirect('home')
    
    context = {
        'total_movies': Movie.objects.count(),
        'total_users': Account.objects.filter(role='user').count(),
        'total_admins': Account.objects.filter(role='admin').count(),
        'total_genres': Genre.objects.count(),
        'total_bookings': Booking.objects.count(),
        'total_reviews': Review.objects.count(),
    }
    
    return render(request, 'Admin/settings.html', context)
