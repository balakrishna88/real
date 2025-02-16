from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import PasswordChangeForm  # Import the form
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
import random
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages

from property.models import CommercialProperty, IndustrialProperty, LandProperty, Property, ResidentialProperty
from .forms import RegistrationForm
from .models import Account
from django.contrib.auth import logout


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create the user (inactive by default)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            
            # Generate a username if not provided (optional)
            username = email.split('@')[0]  # Use the email prefix as the username
            
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,  # Add the username
                email=email,
                phone_number=phone_number,
                password=password,
            )
            user.is_active = False  # User is inactive until OTP verification
            user.save()
            
            # Generate a 6-digit OTP
            otp = random.randint(100000, 999999)
            
            # Store the OTP in the cache (valid for 5 minutes)
            cache_key = f'otp_{user.id}'
            cache.set(cache_key, otp, timeout=300)  # 300 seconds = 5 minutes
            
            # Send the OTP to the user's email using Gmail
            send_mail(
                'Your OTP for Account Activation',
                f'Your OTP for account activation is: {otp}',
                settings.EMAIL_HOST_USER,  # Use the Gmail address from settings
                [email],
                fail_silently=False,
            )
            
            # Redirect to the OTP verification page with email and OTP
            return redirect('verify_otp', email=email, otp=otp)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm()
    
    context = {'form': form}
    return render(request, 'account/register.html', context)


def verify_otp(request, email=None, otp=None):
    if request.method == 'POST':
        email = request.POST.get('email').strip().lower()  # Normalize email
        entered_otp = request.POST.get('otp')

        try:
            # Fetch the user by email (case-insensitive)
            user = Account.objects.get(email__iexact=email)
        except Account.DoesNotExist:
            messages.error(request, 'No account found with this email address.')
            return redirect('forgot_password')

        # Retrieve the stored OTP from the cache
        cache_key = f'otp_{user.id}'
        stored_otp = cache.get(cache_key)

        if stored_otp is None:
            messages.error(request, 'OTP has expired. Please request a new one.')
            return redirect('forgot_password')

        # Validate the entered OTP
        if entered_otp and int(entered_otp) == stored_otp:
            # OTP is valid, activate the user
            user.is_active = True
            user.save()

            # Delete the OTP from the cache
            cache.delete(cache_key)

            messages.success(request, 'Your account has been activated. You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    # Pre-fill the email and OTP if provided
    context = {'email': email, 'otp': otp}
    return render(request, 'account/verify_otp.html', context)


def resend_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email').strip().lower()  # Normalize email

        try:
            # Fetch the user by email (case-insensitive)
            user = Account.objects.get(email__iexact=email)
        except Account.DoesNotExist:
            messages.error(request, 'No account found with this email address.')
            return redirect('register')  # Redirect to registration page if user doesn't exist

        # Generate a new 6-digit OTP
        new_otp = random.randint(100000, 999999)

        # Store the new OTP in the cache (valid for 5 minutes)
        cache_key = f'otp_{user.id}'
        cache.set(cache_key, new_otp, timeout=300)  # 300 seconds = 5 minutes

        # Send the new OTP to the user's email
        send_mail(
            'Your New OTP for Account Activation',
            f'Your new OTP for account activation is: {new_otp}',
            settings.EMAIL_HOST_USER,  # Use the Gmail address from settings
            [email],
            fail_silently=False,
        )

        messages.success(request, 'A new OTP has been sent to your email address.')
        return redirect('verify_otp', email=email, otp=new_otp)

    # If the request method is not POST, redirect to the registration page
    return redirect('register')




def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            # Check if the email exists in the database
            user = Account.objects.get(email=email)
            
            # Check if the user is active
            if user.is_active:
                # Authenticate the user using email and password
                authenticated_user = authenticate(request, email=email, password=password)
                
                if authenticated_user is not None:
                    # Log the user in
                    auth_login(request, authenticated_user)
                    messages.success(request, 'You have been logged in successfully.')
                    return redirect('home')  # Redirect to the dashboard
                else:
                    # Password is incorrect
                    messages.error(request, 'Invalid password.')
            else:
                # User is not active, display a message
                messages.error(request, 'Your account is inactive. Please verify your email.')
        except Account.DoesNotExist:
            # Email does not exist
            messages.error(request, 'No account found with this email address.')
    
    return render(request, 'account/login.html')



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            messages.error(request, 'No account found with this email address.')
            return redirect('forgot_password')
        
        # Generate a 6-digit OTP
        otp = random.randint(100000, 999999)
        
        # Store the OTP in the cache (valid for 5 minutes)
        cache_key = f'password_reset_otp_{user.id}'
        cache.set(cache_key, otp, timeout=300)  # 300 seconds = 5 minutes
        
        # Send the OTP to the user's email
        send_mail(
            'Your OTP for Password Reset',
            f'Your OTP for password reset is: {otp}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        
        messages.success(request, 'An OTP has been sent to your email. Please check your inbox.')
        return redirect('verify_otp', user_id=user.id)
    
    return render(request, 'account/forgot_password.html')

@login_required
def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Validate the new password
        if not new_password or not confirm_password:
            messages.error(request, 'Both fields are required.')
        elif len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        elif new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        else:
            # Check if the new password matches the existing password
            if request.user.check_password(new_password):
                messages.error(request, 'New password must be different from your current password.')
            else:
                # Set the new password
                request.user.set_password(new_password)
                request.user.save()

                # Update the session to prevent the user from being logged out
                update_session_auth_hash(request, request.user)

                messages.success(request, 'Your password has been successfully updated!')
                return redirect('profile')  # Redirect to the user's profile or dashboard

    return render(request, 'account/reset_password.html')









def user_logout(request):
    logout(request)
    return redirect('login')







from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.contenttypes.models import ContentType

@login_required
def dashboard(request):
 
    

    return render(request, 'account/dashboard.html', {
        
    })




from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from property.models import Property, LandProperty, ResidentialProperty, CommercialProperty, IndustrialProperty

@login_required
def dash_user_post(request):
    user = request.user  # Get the logged-in user
    
    # Fetch properties related to the authenticated user
    properties = Property.objects.filter(user=user)
    land_properties = LandProperty.objects.filter(user=user)
    residential_properties = ResidentialProperty.objects.filter(user=user)
    commercial_properties = CommercialProperty.objects.filter(user=user)
    industrial_properties = IndustrialProperty.objects.filter(user=user)
    
    context = {
        'properties': properties,
        'land_properties': land_properties,
        'residential_properties': residential_properties,
        'commercial_properties': commercial_properties,
        'industrial_properties': industrial_properties,
    }
    
    return render(request, 'account/dashboard/dash_user_post.html', context)



@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        # Get the form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')

        # Validate the input
        errors = []
        if not first_name or not last_name or not username or not phone_number or not email:
            errors.append('All fields are required.')
        else:
            # Validate email format
            try:
                validate_email(email)
            except ValidationError:
                errors.append('Please enter a valid email address.')

            # Check if the username is already taken (excluding the current user)
            if User.objects.filter(username=username).exclude(pk=user.pk).exists():
                errors.append('Username is already taken.')

            # Check if the email is already taken (excluding the current user)
            if User.objects.filter(email=email).exclude(pk=user.pk).exists():
                errors.append('Email is already taken.')

        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            # Update the user's details
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.phone_number = phone_number
            user.email = email
            user.save()

            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')

    # Pass the user's details to the template
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'phone_number': user.phone_number,
        'email': user.email,
    }
    return render(request, 'account/profile.html', context)





