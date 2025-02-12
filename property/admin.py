from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.

from .models import IndustrialProperty, Property, LandProperty, Report, ResidentialProperty, CommercialProperty


from django.utils.html import format_html
from .models import Property, PropertyImage

# Inline for Property Images
class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1  # Number of empty forms for new images
    fields = ('image_preview', 'image', 'description', 'created_at')
    readonly_fields = ('image_preview', 'created_at')

    # Method to display an image preview
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.image.url)
        return "No image available"
    image_preview.short_description = "Image Preview"

# Property Admin
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title','id', 'slug', 'deal_type', 'status', 'location', 'listing_date','updated_date', 'is_published', 'featured')
    list_filter = ('deal_type', 'status', 'is_published', 'featured', 'listing_date')
    search_fields = ('title', 'description', 'location', 'contact_phone')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'listing_date'
    ordering = ('-listing_date',)

    inlines = [PropertyImageInline]  # Attach the inline to PropertyAdmin


@admin.register(LandProperty)
class LandPropertyAdmin(PropertyAdmin):
    list_display = PropertyAdmin.list_display + ('property_type', 'total_area', 'area_unit', 'price', 'facing', 'is_corner_plot', 'irrigation_facilities')
    list_filter = PropertyAdmin.list_filter + ('property_type', 'facing', 'is_corner_plot', 'irrigation_facilities')
    search_fields = PropertyAdmin.search_fields + ('soil_type',)

@admin.register(ResidentialProperty)
class ResidentialPropertyAdmin(PropertyAdmin):
    list_display = PropertyAdmin.list_display + ('property_type', 'bedrooms', 'bathrooms', 'furnishing_status', 'price', 'built_up_area', 'total_floors')
    list_filter = PropertyAdmin.list_filter + ('property_type', 'furnishing_status', 'has_garden', 'has_pool')
    search_fields = PropertyAdmin.search_fields + ('bedrooms', 'bathrooms', 'year_built')

@admin.register(CommercialProperty)
class CommercialPropertyAdmin(PropertyAdmin):
    list_display = PropertyAdmin.list_display + ('property_type', 'area', 'furnishing_status', 'price', 'parking')
    list_filter = PropertyAdmin.list_filter + ('property_type', 'furnishing_status', 'parking')
    search_fields = PropertyAdmin.search_fields


@admin.register(IndustrialProperty)
class IndustrialPropertyAdmin(PropertyAdmin):
    list_display = PropertyAdmin.list_display + ('property_type', 'area', 'furnishing_status', 'price', 'parking')
    list_filter = PropertyAdmin.list_filter + ('property_type', 'furnishing_status', 'parking')
    search_fields = PropertyAdmin.search_fields


from .models import PropertyImage, PropertyDocument, PropertyVideo

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property','image', 'description', 'created_at')

@admin.register(PropertyDocument)
class PropertyDocumentAdmin(admin.ModelAdmin):
    list_display = ('property', 'description', 'created_at')

@admin.register(PropertyVideo)
class PropertyVideoAdmin(admin.ModelAdmin):
    list_display = ('property', 'description', 'created_at')




from .models import PropertyActions, PropertyUserTrack

class PropertyActionsAdmin(admin.ModelAdmin):
    # Display property and activity_counts in the list view
    list_display = ('id','property', 'activity_counts')
    
    # Add search functionality by property ID
    search_fields = ('property__id',)
    
    # Order by the property
    ordering = ('property',)

# Register the PropertyActions model with its admin class
admin.site.register(PropertyActions, PropertyActionsAdmin)

class PropertyUserTrackAdmin(admin.ModelAdmin):
    list_display = ('user_email',)
    search_fields = ('user_email',)

admin.site.register(PropertyUserTrack, PropertyUserTrackAdmin)



@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'report_type', 'created_at')
    list_filter = ('report_type', 'created_at')
    search_fields = ('post__id', 'user__username', 'additional_info')
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('post', 'user', 'report_type', 'additional_info')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )




from .models import Comment

# Register Comment model
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Customize the list display to show relevant fields
    list_display = ('property', 'user', 'content', 'created_at', 'updated_at')

    # Enable filtering by property and user
    list_filter = ('property', 'user')

    # Enable searching by content and user
    search_fields = ('content', 'user')

    # Allow the user to edit comments inline with the property admin
    raw_id_fields = ('property',)

    # Display comments in chronological order by default
    ordering = ('-created_at',)
