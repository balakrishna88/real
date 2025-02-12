from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('verify-otp/<str:email>/<str:otp>/', views.verify_otp, name='verify_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),  # Fallback for manual OTP entry
    path('resend-otp/', views.resend_otp, name='resend_otp'),

    path('login/', views.login, name='login'),
    path('accounts/login/', RedirectView.as_view(url='/login/', permanent=True)),
    
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('logout/', views.user_logout, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('dash_user_post/', views.dash_user_post, name='dash_user_post'),
    path('profile/', views.profile, name='profile'),
]