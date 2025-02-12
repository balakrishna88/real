from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

class AccountAdmin(UserAdmin):
    # Fields to display in the list view
    list_display = (
        'email', 'id','first_name', 'last_name', 'username', 'phone_number', 
        'date_joined', 'last_login', 'is_active', 'is_staff'
    )
    
    # Fields that link to the change form
    list_display_links = ('email', 'first_name', 'last_name')
    
    # Read-only fields
    readonly_fields = ('last_login', 'date_joined')
    
    # Default ordering
    ordering = ('-date_joined',)
    
    # Fieldsets for the change form
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': (
            'first_name', 'last_name', 'username', 'phone_number', 
            'profile_picture', 'date_of_birth', 'bio', 'website', 
            'social_media_links'
        )}),
        ('Address Info', {'fields': (
            'country', 'state', 'district', 'location'
        )}),
        ('Permissions', {'fields': (
            'is_active', 'is_staff', 'is_admin', 'is_superadmin'
        )}),
    )
    
    # Add fields for creating a user in the admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name', 'username', 
                'phone_number', 'password1', 'password2'
            ),
        }),
    )
    
    # Filters and horizontal filters (not used here)
    filter_horizontal = ()
    list_filter = ()

# Register the Account model with the custom admin class
admin.site.register(Account, AccountAdmin)