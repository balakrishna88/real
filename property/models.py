from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings  # To access AUTH_USER_MODEL
from django.utils.text import slugify  # To generate slugs from titles
from django.utils import timezone

from property.geocoding import extract_lat_lon_from_gmaps_url

# Define deal types
DEAL_TYPE_CHOICES = [
    ('SELL', 'Sell'),
    ('BUY', 'Buy'),
    ('RENT', 'Rent'),
    ('LEASE', 'Lease'),
    ('SHORT_TERM_RENT', 'Rent Out (Short-Term)'),
    ('AUCTION', 'Auction'),
    ('EXCHANGE', 'Exchange'),
    ('INVEST', 'Invest'),
    ('CO_OWN', 'Co-Own'),
    ('PRE_SALE', 'Pre-Sale/Under Construction'),
    ('PG_HOSTEL', 'PG/Hostel'),
    ('COMMERCIAL', 'Commercial Use'),
    ('AGRICULTURAL', 'Agricultural/Farm Land'),
    ('VACATION_HOME', 'Vacation Home'),
    ('FORECLOSURE', 'Foreclosure/Distressed Properties'),
    ('CO_LIVING', 'Co-Living Spaces'),
]

STATUS_CHOICES = [
    ('AVAILABLE', 'Available'),
    ('PENDING', 'Pending'),
    ('SOLD', 'Sold'),
    ('RENTED', 'Rented'),
    ('CLOSED', 'Closed'),
]

class Property(models.Model):
    # Link to the user who created the property
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties')

    # Required fields
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)  # SEO-friendly URL
    contact_phone = models.CharField(max_length=20)

    # Optional fields
    description = models.TextField(max_length=1000, blank=True, null=True)  # Limit description to 1000 characters
    location = models.CharField(max_length=255, blank=True, null=True)  # General location (e.g., neighborhood, city)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    # Detailed address fields with default values
    country = models.CharField(max_length=100, blank=True, null=True)  # Country
    state = models.CharField(max_length=100, blank=True, null=True)  # State or province
    district = models.CharField(max_length=100, blank=True, null=True)  # District
    subdivision = models.CharField(max_length=100, blank=True, null=True)  # Subdivision (e.g., mandal, sub-district)
    village = models.CharField(max_length=100, blank=True, null=True)  # Village or town
    pincode = models.CharField(max_length=10, blank=True, null=True)  # Postal code or ZIP code

    # New deal_type field
    deal_type = models.CharField(max_length=50, choices=DEAL_TYPE_CHOICES, default='SELL')

    # Other fields
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='AVAILABLE')  # Tracks availability status
    listing_date = models.DateField(auto_now_add=True, null=True)  # Automatically set when created (IST)
    updated_date = models.DateTimeField(auto_now=True)   # Automatically updated on every save
    is_published = models.BooleanField(default=True)  # True if property is published
    featured = models.BooleanField(default=False)  # Highlight featured properties
    contact_email = models.EmailField(blank=True, null=True)  # Contact email for inquiries

    class Meta:
        ordering = ['-listing_date']  # Default ordering for queries

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Automatically generate the slug from the title if it's not provided
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure the slug is unique
            original_slug = self.slug
            counter = 1
            while self.__class__.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1

    # Generate latitude and longitude from the location field if it's a Google Maps URL
        if self.location and (not self.latitude or not self.longitude):
            latitude, longitude = extract_lat_lon_from_gmaps_url(self.location)
            if latitude and longitude:
                self.latitude = latitude
                self.longitude = longitude

        super().save(*args, **kwargs)




class LandProperty(Property):
    # Define property types for land
    PROPERTY_TYPE_CHOICES = [
        ('LAND', 'Land'),
        ('PLOT', 'Plot'),
        ('FARM_LAND', 'Farm Land'),
    ]

    # Define facing directions
    FACING_CHOICES = [
        ('NORTH', 'North'),
        ('SOUTH', 'South'),
        ('EAST', 'East'),
        ('WEST', 'West'),
        ('NORTH_EAST', 'North-East'),
        ('NORTH_WEST', 'North-West'),
        ('SOUTH_EAST', 'South-East'),
        ('SOUTH_WEST', 'South-West'),
    ]

    # Define area units
    AREA_UNIT_CHOICES = [
        ('SQFT', 'Square Feet'),
        ('ACRES', 'Acres'),
        ('HECTARES', 'Hectares'),
        ('SQM', 'Square Meters'),
    ]

    # Fields
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES, default='LAND')
    total_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Area value
    area_unit = models.CharField(max_length=10, choices=AREA_UNIT_CHOICES, default='SQFT')  # Unit of measurement
    price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)  # Price of the property

    nearby_amenities = models.CharField(max_length=500, blank=True, null=True)
    nearby = models.CharField(max_length=500, blank=True, null=True)
    distance_from_road = models.CharField(max_length=500, blank=True, null=True)

    has_water = models.BooleanField(default=False)  # Water availability
    has_electricity = models.BooleanField(default=False)  # Electricity availability
    is_corner_plot = models.BooleanField(default=False)  # Specific to Plot
    soil_type = models.CharField(max_length=100, blank=True, null=True)  # Specific to Farm Land
    irrigation_facilities = models.BooleanField(default=False)  # Specific to Farm Land
    facing = models.CharField(max_length=50, choices=FACING_CHOICES, blank=True, null=True)  # Facing direction

    def __str__(self):
        return f"{self.title} ({self.get_property_type_display()})"

    def get_area_display(self):
        """
        Helper method to return the total area with the unit.
        """
        if self.total_area and self.area_unit:
            return f"{self.total_area} {self.get_area_unit_display()}"
        return "Area not specified"

    def get_price_display(self):
        """
        Helper method to return a formatted price.
        """
        if self.price:
            return f"${self.price:,.2f}"  # Format price with commas and two decimal places
        return "Price not specified"
    
    




class ResidentialProperty(Property):
    # Define property types for residential properties
    PROPERTY_TYPE_CHOICES = [
        ('HOUSE', 'House'),
        ('APARTMENT', 'Apartment'),
        ('VILLA', 'Villa'),
        ('BUNGALOW', 'Bungalow'),
        ('RESORT_PROPERTY', 'Resort Property'),
        ('FARM_HOUSE', 'Farm House')  # Corrected Farm House choice
    ]

    # Define furnishing statuses
    FURNISHING_CHOICES = [
        ('FURNISHED', 'Furnished'),
        ('SEMI_FURNISHED', 'Semi-Furnished'),
        ('UNFURNISHED', 'Unfurnished'),
    ]

    # Define parking availability
    PARKING_CHOICES = [
        ('NONE', 'No Parking'),
        ('COVERED', 'Covered Parking'),
        ('OPEN', 'Open Parking'),
    ]

    # Fields
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES, default='HOUSE')
    bedrooms = models.PositiveIntegerField(blank=True, null=True)  # Number of bedrooms
    bathrooms = models.PositiveIntegerField(blank=True, null=True)  # Number of bathrooms
    furnishing_status = models.CharField(max_length=20, choices=FURNISHING_CHOICES, default='UNFURNISHED')
    parking = models.CharField(max_length=20, choices=PARKING_CHOICES, default='NONE')  # Parking type
    built_up_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Built-up area
    total_floors = models.PositiveIntegerField(blank=True, null=True)  # Total floors in the building
    floor_number = models.PositiveIntegerField(blank=True, null=True)  # Floor number (for apartments)
    balcony_count = models.PositiveIntegerField(blank=True, null=True)  # Number of balconies
    has_garden = models.BooleanField(default=False)  # Garden availability (specific to Villas/Bungalows)
    has_pool = models.BooleanField(default=False)  # Pool availability (specific to Villas/Resorts)
    year_built = models.PositiveIntegerField(blank=True, null=True)  # Construction year
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)  # Property price

    nearby_amenities = models.CharField(max_length=500, blank=True, null=True)
    nearby = models.CharField(max_length=500, blank=True, null=True)
    distance_from_road = models.CharField(max_length=500, blank=True, null=True)
    has_security = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.get_property_type_display()})"

    def get_built_up_area_display(self):
        """
        Helper method to return the built-up area with units (sq ft).
        """
        if self.built_up_area:
            return f"{self.built_up_area} Sq. Ft."
        return "Area not specified"

    def get_furnishing_display(self):
        """
        Helper method to return the furnishing status.
        """
        return self.get_furnishing_status_display()

    def get_price_display(self):
        """
        Helper method to return the price formatted with currency symbol (₹).
        """
        if self.price:
            return f"₹ {self.price:,.2f}"  # Formats the price with commas and decimal points
        return "Price not specified"



class CommercialProperty(Property):
    # Define property types for commercial properties
    PROPERTY_TYPE_CHOICES = [
        ('SHOP', 'Shop'),
        ('OFFICE_SPACE', 'Office Space'),
        ('WAREHOUSE', 'Warehouse'),
        ('COMMERCIAL_PROPERTY', 'Commercial Property'),
    ]

    # Define furnishing statuses
    FURNISHING_CHOICES = [
        ('FURNISHED', 'Furnished'),
        ('SEMI_FURNISHED', 'Semi-Furnished'),
        ('UNFURNISHED', 'Unfurnished'),
    ]

    # Define parking availability
    PARKING_CHOICES = [
        ('NONE', 'No Parking'),
        ('COVERED', 'Covered Parking'),
        ('OPEN', 'Open Parking'),
    ]

    # Fields
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES, default='SHOP')
    area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Area of the property in sq ft
    furnishing_status = models.CharField(max_length=20, choices=FURNISHING_CHOICES, default='UNFURNISHED')
    parking = models.CharField(max_length=20, choices=PARKING_CHOICES, default='NONE')  # Parking type
    year_built = models.PositiveIntegerField(blank=True, null=True)  # Year of construction
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)  # Property price
    total_floors = models.PositiveIntegerField(blank=True, null=True)  # Total floors in the building
    floor_number = models.PositiveIntegerField(blank=True, null=True)  # Floor number (for office spaces)
    has_air_conditioning = models.BooleanField(default=False)  # Air conditioning availability
    has_elevator = models.BooleanField(default=False)  # Elevator availability
    is_renovated = models.BooleanField(default=False)  # Whether the property has been renovated

    nearby_amenities = models.CharField(max_length=500, blank=True, null=True)
    nearby = models.CharField(max_length=500, blank=True, null=True)
    distance_from_road = models.CharField(max_length=500, blank=True, null=True)
    has_security = models.BooleanField(default=False)
    power_backup = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.get_property_type_display()})"

    def get_area_display(self):
        """
        Helper method to return the area with units (sq ft).
        """
        if self.area:
            return f"{self.area} Sq. Ft."
        return "Area not specified"

    def get_furnishing_display(self):
        """
        Helper method to return the furnishing status.
        """
        return self.get_furnishing_status_display()

    def get_price_display(self):
        """
        Helper method to return the price formatted with currency symbol (₹).
        """
        if self.price:
            return f"₹ {self.price:,.2f}"  # Formats the price with commas and decimal points
        return "Price not specified"




class IndustrialProperty(Property):
    # Define property types for industrial properties
    PROPERTY_TYPE_CHOICES = [
        ('INDUSTRIAL_PROPERTY', 'Industrial Property'),
        ('BUILDING', 'Building'),
    ]

    # Define furnishing statuses
    FURNISHING_CHOICES = [
        ('FURNISHED', 'Furnished'),
        ('SEMI_FURNISHED', 'Semi-Furnished'),
        ('UNFURNISHED', 'Unfurnished'),
    ]

    # Define parking availability
    PARKING_CHOICES = [
        ('NONE', 'No Parking'),
        ('COVERED', 'Covered Parking'),
        ('OPEN', 'Open Parking'),
    ]

    # Fields
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES, default='INDUSTRIAL_PROPERTY')
    area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Area in sq ft
    furnishing_status = models.CharField(max_length=20, choices=FURNISHING_CHOICES, default='UNFURNISHED')
    parking = models.CharField(max_length=20, choices=PARKING_CHOICES, default='NONE')  # Parking type
    year_built = models.PositiveIntegerField(blank=True, null=True)  # Year of construction
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)  # Property price
    total_floors = models.PositiveIntegerField(blank=True, null=True)  # Total number of floors in the building
    floor_number = models.PositiveIntegerField(blank=True, null=True)  # Specific floor number (for buildings)
    has_lift = models.BooleanField(default=False)  # Lift/Elevator availability
    has_security = models.BooleanField(default=False)  # Security availability (for industrial properties)

    nearby_amenities = models.CharField(max_length=500, blank=True, null=True)
    nearby = models.CharField(max_length=500, blank=True, null=True)
    distance_from_road = models.CharField(max_length=500, blank=True, null=True)
    power_backup = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.get_property_type_display()})"

    def get_area_display(self):
        """
        Helper method to return the area with units (sq ft).
        """
        if self.area:
            return f"{self.area} Sq. Ft."
        return "Area not specified"

    def get_furnishing_display(self):
        """
        Helper method to return the furnishing status.
        """
        return self.get_furnishing_status_display()

    def get_price_display(self):
        """
        Helper method to return the price formatted with currency symbol (₹).
        """
        if self.price:
            return f"₹ {self.price:,.2f}"  # Formats the price with commas and decimal points
        return "Price not specified"



#images

import os
from uuid import uuid4
from django.utils.timezone import now
from django.core.files.storage import default_storage
from django.db import models

def dynamic_file_upload(instance, filename):
    """
    Dynamically generate file paths based on the model class name and instance fields.
    """
    ext = filename.split('.')[-1]  # Get the file extension
    file_type = instance.__class__.__name__.lower()  # Use model class name to determine folder
    property_type = getattr(instance.property, 'property_type', 'UNKNOWN').replace(' ', '_')
    deal_type = getattr(instance.property, 'deal_type', 'UNKNOWN').replace(' ', '_')
    folder_name = f"{file_type}_files"  # Use model name to determine folder

    # Base file name
    base_filename = f"{property_type}_{deal_type}"
    
    # Add timestamp for traceability
    timestamp = now().strftime('%Y%m%d_%H%M%S')
    unique_id = uuid4().hex[:8]  # Shortened UUID for uniqueness

    # Combine base filename
    file_name = f"{base_filename}_{unique_id}_{timestamp}.{ext}"
    file_path = os.path.join(folder_name, file_name)

    # Ensure unique file name by appending an incrementing number if it exists
    counter = 1
    while default_storage.exists(file_path):
        file_name = f"{base_filename}_{unique_id}_{timestamp}_{counter}.{ext}"
        file_path = os.path.join(folder_name, file_name)
        counter += 1

    return file_path

class PropertyImage(models.Model):
    property = models.ForeignKey('Property', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=dynamic_file_upload)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.title}"

class PropertyDocument(models.Model):
    property = models.ForeignKey('Property', related_name='documents', on_delete=models.CASCADE)
    document = models.FileField(upload_to=dynamic_file_upload)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for {self.property.title}"

class PropertyVideo(models.Model):
    property = models.ForeignKey('Property', related_name='videos', on_delete=models.CASCADE)
    video = models.FileField(upload_to=dynamic_file_upload)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video for {self.property.title}"
    



class PropertyActions(models.Model):
    """
    Model to track activity counts (likes, shares, views, comments, reports) for each property.
    Uses a nested structure to store counts for authenticated users and guests.
    """
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='actions')

    # Nested structure for activity counts
    activity_counts = models.JSONField(
        default=dict,
        help_text="Nested structure to store activity counts for authenticated users and guests."
    )

    def __str__(self):
        # Use the property's title instead of ID for a more descriptive representation
        return f"Actions for Property: {self.property.title}"

    def update_count(self, activity_type, is_auth_user=True, increment=True):
        """
        Helper method to increment or decrement activity counts.
        """
        user_type = 'auth' if is_auth_user else 'guest'
        key = f"{user_type}_{activity_type}"

        # Initialize the count if it doesn't exist
        if key not in self.activity_counts:
            self.activity_counts[key] = 0

        # Increment or decrement the count
        if increment:
            self.activity_counts[key] += 1
        else:
            self.activity_counts[key] = max(0, self.activity_counts[key] - 1)  # Ensure count doesn't go below 0

        self.save()

        # Optionally, add logging for debugging purposes
        print(f"Updated {activity_type} for property {self.property.title}: {self.activity_counts[key]}")


class PropertyUserTrack(models.Model):
    """
    Model to track individual activities (e.g., likes, shares, views, comments, reports) for authenticated users.
    Uses nested structures to store liked, shared, viewed, commented, and reported properties.
    """
    user_email = models.EmailField(unique=True, help_text="Email of the authenticated user.")

    # Nested structure to store liked properties
    property_like = models.JSONField(
        default=list,
        help_text="List of Property IDs liked by the user."
    )

    # Nested structure to store shared properties
    property_share = models.JSONField(
        default=list,
        help_text="List of Property IDs shared by the user."
    )

    # Nested structure to store viewed properties
    property_view = models.JSONField(
        default=list,
        help_text="List of Property IDs viewed by the user."
    )

    # Nested structure to store commented properties
    property_comment = models.JSONField(
        default=list,
        help_text="List of Property IDs commented by the user."
    )

    # Nested structure to store reported properties
    property_report = models.JSONField(
        default=list,
        help_text="List of Property IDs reported by the user."
    )

    property_favourite = models.JSONField(
        default=list,
        help_text="List of Property IDs marked as favourites by the user."
    )

    def __str__(self):
        return f"User Track for {self.user_email}"

    def add_liked_property(self, property_id):
        """
        Helper method to add a liked property to the nested list.
        """
        if property_id not in self.property_like:
            self.property_like.append(property_id)
            self.save()

    def remove_liked_property(self, property_id):
        """
        Helper method to remove a liked property from the nested list.
        """
        if property_id in self.property_like:
            self.property_like.remove(property_id)
            self.save()

    def add_shared_property(self, property_id):
        """
        Helper method to add a shared property to the nested list.
        """
        if property_id not in self.property_share:
            self.property_share.append(property_id)
            self.save()

    def add_viewed_property(self, property_id):
        """
        Helper method to add a viewed property to the nested list.
        """
        if property_id not in self.property_view:
            self.property_view.append(property_id)
            self.save()

    def add_commented_property(self, property_id):
        """
        Helper method to add a commented property to the nested list.
        """
        if property_id not in self.property_comment:
            self.property_comment.append(property_id)
            self.save()

    def add_reported_property(self, property_id):
        """
        Helper method to add a reported property to the nested list.
        """
        if property_id not in self.property_report:
            self.property_report.append(property_id)
            self.save()

    
    def add_favourite_property(self, property_id):
        """
        Helper method to add a favourite property to the nested list.
        """
        if property_id not in self.property_favourite:
            self.property_favourite.append(property_id)
            self.save()

    def remove_favourite_property(self, property_id):
        """
        Helper method to remove a favourite property from the nested list.
        """
        if property_id in self.property_favourite:
            self.property_favourite.remove(property_id)
            self.save()




class Report(models.Model):
    # Choices for the type of report
    REPORT_CHOICES = [
        ('spam', 'Spam'),
        ('expired', 'Expired'),
        ('no_response', 'No Response'),
        ('other', 'Other'),
    ]

    post = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reports')
    user = models.CharField(max_length=150, blank=True, null=True)  # Store username or "guest"
    report_type = models.CharField(max_length=20, choices=REPORT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    additional_info = models.TextField(blank=True, null=True, help_text="Additional information about the report.")

    def __str__(self):
        return f"Report by {self.user or 'guest'} on {self.post.id} ({self.report_type})"
    


from django.db import models

class Comment(models.Model):
    property = models.ForeignKey('Property', on_delete=models.CASCADE, related_name="propertycomments")
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    user = models.CharField(max_length=100, default="guest", blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user} on Property ID {self.property.id}"

    class Meta:
        ordering = ['created_at']
