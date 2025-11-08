from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account


class RegisterForm(UserCreationForm):
    """
    User registration form
    """
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    
    class Meta:
        model = Account
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter username'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })


class LoginForm(forms.Form):
    """
    User login form
    """
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter password'
    }))


class UpdateProfileForm(forms.ModelForm):
    """
    Update user profile form
    """
    class Meta:
        model = Account
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email'
            }),
        }


class ChangePasswordForm(forms.Form):
    """
    Change password form
    """
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter current password'
    }))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter new password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm new password'
    }))
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError('New passwords do not match!')
        
        return cleaned_data


class AdminCreateAccountForm(UserCreationForm):
    """
    Admin form to create new accounts with role selection
    """
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter email'
    }))
    role = forms.ChoiceField(choices=Account.ROLE_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    
    class Meta:
        model = Account
        fields = ['username', 'email', 'password1', 'password2', 'role']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter username'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super(AdminCreateAccountForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })


class AdminEditAccountForm(forms.ModelForm):
    """
    Admin form to edit existing accounts
    """
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Leave blank to keep current password'
    }))
    
    class Meta:
        model = Account
        fields = ['username', 'email', 'role', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email'
            }),
            'role': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
