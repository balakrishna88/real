# forms.py
from django import forms
from .models import Group

class GroupSettingsForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['description', 'logo', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-3 py-2 border rounded-md'}),
            'status': forms.Select(attrs={'class': 'px-3 py-2 border rounded-md'}),
        }