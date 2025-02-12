from django import forms
from django.forms import ClearableFileInput
from .models import LandProperty, Property, ResidentialProperty, CommercialProperty, IndustrialProperty

# ------------------- Image, Document, and Video Forms -------------------
class PropertyImageForm(forms.Form):
    images = forms.FileField(
        widget=ClearableFileInput(attrs={'allow_multiple_selected': True}),
        label='Upload Images',
        required=False
    )

class PropertyDocumentForm(forms.Form):
    documents = forms.FileField(
        widget=ClearableFileInput(attrs={'allow_multiple_selected': True}),
        label='Upload Documents',
        required=False
    )

class PropertyVideoForm(forms.Form):
    videos = forms.FileField(
        widget=ClearableFileInput(attrs={'allow_multiple_selected': True}),
        label='Upload Videos',
        required=False
    )

# ------------------------- Property Forms ------------------------------
class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'slug', 'contact_phone', 'description', 'location',
            'country', 'state', 'district', 'subdivision', 'village', 
            'pincode', 'deal_type', 'is_published', 'featured', 'contact_email'
        ]

class LandPropertyForm(forms.ModelForm):
    class Meta:
        model = LandProperty
        fields = [
            'title', 'slug', 'contact_phone', 'description', 'location',
            'country', 'state', 'district', 'subdivision', 'village', 
            'pincode', 'deal_type', 'is_published', 'featured', 'contact_email', 
            'property_type', 'total_area', 'area_unit', 'price',
            'has_water', 'has_electricity', 'is_corner_plot', 
            'soil_type', 'irrigation_facilities', 'facing','nearby_amenities', 'nearby','distance_from_road'
        ]
        

class ResidentialPropertyForm(forms.ModelForm):
    class Meta:
        model = ResidentialProperty
        fields = [
            'title', 'slug', 'contact_phone', 'description', 'location',
            'country', 'state', 'district', 'subdivision', 'village',
            'pincode', 'deal_type', 'is_published', 'featured', 'contact_email',
            'property_type', 'bedrooms', 'bathrooms', 'furnishing_status',
            'parking', 'built_up_area', 'total_floors', 'floor_number',
            'balcony_count', 'has_garden', 'has_pool', 'year_built', 'price', 'nearby_amenities', 'nearby','distance_from_road', 'has_security'
        ]
    

class CommercialPropertyForm(forms.ModelForm):
    class Meta:
        model = CommercialProperty
        fields = [
            'title', 'slug', 'contact_phone', 'description', 'location',
            'country', 'state', 'district', 'subdivision', 'village',
            'pincode', 'deal_type', 'is_published', 'featured', 
            'contact_email', 'property_type', 'area', 'furnishing_status', 
            'parking', 'year_built', 'price', 'total_floors', 'floor_number',
            'has_air_conditioning', 'has_elevator', 'is_renovated' , 'nearby_amenities', 'nearby','distance_from_road', 'has_security'
        ]

class IndustrialPropertyForm(forms.ModelForm):
    class Meta:
        model = IndustrialProperty
        fields = [
            'title', 'slug', 'contact_phone', 'description', 'location',
            'country', 'state', 'district', 'subdivision', 'village', 
            'pincode', 'deal_type', 'is_published', 'featured',
            'contact_email', 'property_type', 'area', 'furnishing_status', 
            'parking', 'year_built', 'price', 'total_floors', 'floor_number',
            'has_lift', 'has_security' , 'nearby_amenities', 'nearby','distance_from_road'
        ]
