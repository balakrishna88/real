from rest_framework import serializers
from property.models import Comment, CommercialProperty, IndustrialProperty, Property, LandProperty, PropertyActions, PropertyUserTrack, Report, ResidentialProperty

class PropertySerializer(serializers.ModelSerializer):
    # Nested serializers for child models
    landproperty = serializers.SerializerMethodField()
    residentialproperty = serializers.SerializerMethodField()
    commercialproperty = serializers.SerializerMethodField()
    industrialproperty = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = [
            'id', 'user', 'title', 'slug', 'contact_phone', 'description', 
            'location', 'country', 'state', 'district', 'subdivision', 'village', 
            'pincode', 'deal_type', 'status', 'listing_date', 'updated_date', 
            'is_published', 'featured', 'contact_email',
            'landproperty', 'residentialproperty', 'commercialproperty', 'industrialproperty'
        ]

    def get_landproperty(self, obj):
        # Check if the object is an instance of LandProperty
        if isinstance(obj, LandProperty):
            return LandPropertySerializer(obj).data
        return None

    def get_residentialproperty(self, obj):
        # Check if the object is an instance of ResidentialProperty
        if isinstance(obj, ResidentialProperty):
            return ResidentialPropertySerializer(obj).data
        return None

    def get_commercialproperty(self, obj):
        # Check if the object is an instance of CommercialProperty
        if isinstance(obj, CommercialProperty):
            return CommercialPropertySerializer(obj).data
        return None

    def get_industrialproperty(self, obj):
        # Check if the object is an instance of IndustrialProperty
        if isinstance(obj, IndustrialProperty):
            return IndustrialPropertySerializer(obj).data
        return None


class LandPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = LandProperty
        fields = '__all__'


class ResidentialPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResidentialProperty
        fields = '__all__'


class CommercialPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommercialProperty
        fields = '__all__'


class IndustrialPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustrialProperty
        fields = '__all__'




class PropertyActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyActions
        fields = '__all__'

class PropertyUserTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyUserTrack
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'