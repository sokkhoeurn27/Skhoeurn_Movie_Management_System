from django import forms
from .models import Movie, Genre, Booking, Review


class MovieForm(forms.ModelForm):
    """
    Form for creating/editing movies
    """
    class Meta:
        model = Movie
        fields = ['title', 'description', 'genre', 'duration', 'release_date', 
                  'director', 'cast', 'poster', 'trailer_url', 'rating', 
                  'status', 'ticket_price', 'available_seats']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter movie title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter movie description'
            }),
            'genre': forms.Select(attrs={
                'class': 'form-control'
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Duration in minutes'
            }),
            'release_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'director': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter director name'
            }),
            'cast': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Enter cast names (comma-separated)'
            }),
            'poster': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'trailer_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter trailer URL'
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0',
                'max': '10'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'ticket_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Enter ticket price'
            }),
            'available_seats': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter available seats'
            }),
        }


class GenreForm(forms.ModelForm):
    """
    Form for creating/editing genres
    """
    class Meta:
        model = Genre
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter genre name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter genre description (optional)'
            }),
        }


class BookingForm(forms.ModelForm):
    """
    Form for booking movie tickets
    """
    class Meta:
        model = Booking
        fields = ['show_date', 'show_time', 'number_of_seats', 'payment_method']
        widgets = {
            'show_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'show_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'number_of_seats': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Enter number of seats'
            }),
            'payment_method': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter payment method (e.g., Credit Card, Cash)'
            }),
        }


class ReviewForm(forms.ModelForm):
    """
    Form for creating/editing movie reviews
    """
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)], attrs={
                'class': 'form-control'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your review here...'
            }),
        }


class BookingStatusForm(forms.ModelForm):
    """
    Form for updating booking status (Admin)
    """
    class Meta:
        model = Booking
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


class MovieSearchForm(forms.Form):
    """
    Form for searching movies
    """
    search = forms.CharField(required=False, max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Search by title, director, or cast...'
    }))
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        required=False,
        empty_label="All Genres",
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
