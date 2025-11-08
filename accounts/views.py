from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account
from .forms import RegisterForm, LoginForm, UpdateProfileForm, ChangePasswordForm


def register_view(request):
    """
    User registration view
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'user'  # Automatically set to 'user' for public registration
            user.save()
            messages.success(request, 'Account created successfully! Please login.')
            # Redirect to home with a flag to open login modal
            return redirect('home')
        else:
            # Form errors will be displayed in the template
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            return redirect('home')
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """
    User login view
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                
                # Redirect based on role
                if user.is_admin():
                    return redirect('admin_dashboard')
                else:
                    return redirect('home')
            else:
                messages.error(request, 'Invalid username or password!')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    """
    User logout view
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')


@login_required
def profile_view(request):
    """
    User profile view - Shows only user information
    Redirects admins to their dedicated profile page
    """
    user = request.user
    
    # Redirect admins to admin profile
    if user.is_admin():
        return redirect('admin_profile')
    
    context = {
        'user': user,
    }
    
    return render(request, 'profile.html', context)


@login_required
def my_bookings_view(request):
    """
    User bookings view - Shows all user bookings
    """
    bookings = request.user.bookings.all().order_by('-booking_date')
    
    context = {
        'bookings': bookings,
    }
    
    return render(request, 'my_bookings.html', context)


@login_required
def my_reviews_view(request):
    """
    User reviews view - Shows all user reviews
    """
    reviews = request.user.reviews.all().order_by('-created_at')
    
    context = {
        'reviews': reviews,
    }
    
    return render(request, 'my_reviews.html', context)


@login_required
def update_profile(request):
    """
    Update user profile
    """
    if request.method == 'POST':
        profile_form = UpdateProfileForm(request.POST, instance=request.user)
        password_form = ChangePasswordForm(request.POST)
        
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
        
        if password_form.is_valid():
            old_password = password_form.cleaned_data['old_password']
            new_password = password_form.cleaned_data['new_password']
            
            if request.user.check_password(old_password):
                request.user.set_password(new_password)
                request.user.save()
                messages.success(request, 'Password changed successfully!')
                return redirect('login')  # Redirect to login after password change
            else:
                messages.error(request, 'Current password is incorrect!')
        
        return redirect('profile')
    
    return redirect('profile')
