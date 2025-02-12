from django import forms
from django.core.exceptions import ValidationError
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password',
            'class': 'form-control',
        }),
        min_length=8,  # Minimum password length
        help_text="Password must be at least 8 characters long.",
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm password',
            'class': 'form-control',
        }),
    )
    
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        
        # Set placeholders and classes for all fields
        placeholders = {
            'first_name': 'Enter First Name',
            'last_name': 'Enter Last Name',
            'phone_number': 'Enter Phone Number',
            'email': 'Enter Email',
        }
        
        for field in self.fields:
            if field in placeholders:
                self.fields[field].widget.attrs['placeholder'] = placeholders[field]
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['required'] = True  # Make all fields required
    
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match!")
        
        # Additional password validation
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        
        return cleaned_data
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Account.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if Account.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("An account with this phone number already exists.")
        return phone_number