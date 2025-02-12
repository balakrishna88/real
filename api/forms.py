# forms.py

from django import forms
from property.models import CommercialProperty, Property, LandProperty, ResidentialProperty

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'contact_phone', 'description', 'location', 'country', 'state', 'district', 'subdivision', 'village', 'pincode', 'deal_type', 'status', 'is_published', 'featured', 'contact_email']

class LandPropertyForm(PropertyForm):
    class Meta:
        model = LandProperty
        fields = PropertyForm.Meta.fields + ['property_type', 'total_area', 'area_unit', 'price', 'has_water', 'has_electricity', 'is_corner_plot', 'soil_type', 'irrigation_facilities', 'facing', 'nearby_amenities', 'nearby','distance_from_road']



from django import forms
from property.models import ResidentialProperty

class ResidentialPropertyForm(forms.ModelForm):
    class Meta:
        model = ResidentialProperty
        fields = [
            'title',
            'contact_phone',
            'description',
            'location',
            'country',
            'state',
            'district',
            'subdivision',
            'village',
            'pincode',
            'deal_type',
            'status',
            'is_published',
            'featured',
            'contact_email',
            'property_type',
            'bedrooms',
            'bathrooms',
            'furnishing_status',
            'parking',
            'built_up_area',
            'total_floors',
            'floor_number',
            'balcony_count',
            'has_garden',
            'has_pool',
            'year_built',
            'price',
            'nearby_amenities', 'nearby','distance_from_road', 'has_security'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class CommercialPropertyForm(forms.ModelForm):
    class Meta:
        model = CommercialProperty
        fields = [
            'title',
            'contact_phone',
            'description',
            'location',
            'country',
            'state',
            'district',
            'subdivision',
            'village',
            'pincode',
            'deal_type',
            'status',
            'is_published',
            'featured',
            'contact_email',
            'property_type',
            'area',
            'furnishing_status',
            'parking',
            'year_built',
            'price',
            'total_floors',
            'floor_number',
            'has_air_conditioning',
            'has_elevator',
            'is_renovated',
            'nearby_amenities', 'nearby','distance_from_road', 'has_security'
            
        ]

   



from django import forms
from property.models import IndustrialProperty


class IndustrialPropertyForm(forms.ModelForm):
    class Meta:
        model = IndustrialProperty
        fields = [
            'title',
            'contact_phone',
            'description',
            'location',
            'country',
            'state',
            'district',
            'subdivision',
            'village',
            'pincode',
            'deal_type',
            'status',
            'is_published',
            'featured',
            'contact_email',
            'property_type',
            'area',
            'furnishing_status',
            'parking',
            'year_built',
            'price',
            'total_floors',
            'floor_number',
            'has_lift',
            'has_security' , 'nearby_amenities', 'nearby','distance_from_road'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'location': forms.TextInput(attrs={'placeholder': 'Enter a general location'}),
            'contact_phone': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
            'pincode': forms.TextInput(attrs={'placeholder': 'Enter postal code'}),
            'price': forms.NumberInput(attrs={'step': 0.01}),
            'year_built': forms.NumberInput(attrs={'placeholder': 'e.g., 2020'}),
        }




# forms.py
from django import forms
from property.models import Report, Comment

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['report_type', 'additional_info']
        widgets = {
            'report_type': forms.Select(attrs={'class': 'form-control'}),
            'additional_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add a comment...'}),
        }