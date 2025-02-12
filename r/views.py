from django.shortcuts import render

from property.models import CommercialProperty, IndustrialProperty, LandProperty, Property, PropertyActions, ResidentialProperty

def home(request):
    properties = Property.objects.filter(is_published=True).order_by('-updated_date')[:6]

    # Fetch unique states, subdivisions, and villages
        # Fetch unique states, districts, subdivisions, and villages
    states = Property.objects.exclude(state__isnull=True).values_list('state', flat=True).distinct()
    districts = Property.objects.exclude(district__isnull=True).values_list('district', flat=True).distinct()
    subdivisions = Property.objects.exclude(subdivision__isnull=True).values_list('subdivision', flat=True).distinct()
    villages = Property.objects.exclude(village__isnull=True).values_list('village', flat=True).distinct()

    # Convert to sets to ensure uniqueness (optional, as distinct() already ensures uniqueness in the database query)
    states = set(states)
    districts = set(districts)
    subdivisions = set(subdivisions)
    villages = set(villages)

    # If you want the results as sorted lists:
    states = sorted(states)
    districts = sorted(districts)
    subdivisions = sorted(subdivisions)
    villages = sorted(villages)


    # Attach action stats (views, likes, shares) and determine property type
    for property in properties:
        try:
            actions = property.actions  # Get the related PropertyActions object
            property.views = actions.activity_counts.get("auth_views", 0) + actions.activity_counts.get("guest_views", 0)
            property.likes = actions.activity_counts.get("auth_likes", 0) + actions.activity_counts.get("guest_likes", 0)
            property.shares = actions.activity_counts.get("auth_shares", 0) + actions.activity_counts.get("guest_shares", 0)
        except PropertyActions.DoesNotExist:
            property.views = 0
            property.likes = 0
            property.shares = 0

        # Determine the child class dynamically using hasattr()
        if hasattr(property, 'landproperty'):
            property.property_type = "Land"
        elif hasattr(property, 'residentialproperty'):
            property.property_type = "Residential"
        elif hasattr(property, 'commercialproperty'):
            property.property_type = "Commercial"
        elif hasattr(property, 'industrialproperty'):
            property.property_type = "Industrial"
        else:
            property.property_type = "General"

    return render(request, 'index.html', {'properties': properties,'states': states,
        'subdivisions': subdivisions, 'districts': districts,
        'villages': villages})

import requests
import re
def expand_gmap_url(request):
    context = {"error_message": None}
    
    if request.method == "POST":
        short_url = request.POST.get("short_url", "").strip()
        if short_url:
            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                full_url = requests.get(short_url, headers=headers, allow_redirects=True).url
                
                if "maps/search/" in full_url:
                    extracted = re.search(r"maps/search/(.*?)(coh%|$)", full_url)
                    location = extracted.group(1) if extracted else None
                    
                    if location and "," in location:
                        lat_raw, lon_raw = location.split(",")[:2]
                        extract_coord = lambda val: val[max(0, val.find(".")-2):val.find(".")+7] if "." in val else "N/A"
                        context.update({
                            "full_url": full_url, "location": location,
                            "latitude": extract_coord(lat_raw), "longitude": extract_coord(lon_raw)
                        })
            except requests.RequestException:
                context["error_message"] = "Failed to fetch the full URL. Try again."

    return render(request, "expand_url.html", context)




from geopy.distance import geodesic
from django.shortcuts import render
from property.models import Property

from geopy.distance import geodesic
from django.shortcuts import render
from property.models import Property

def nearby_properties(request):
    user_location = (17.606108, 78.586269)  # Fixed coordinates (change as needed)
    radius_km = 100  # Search radius

    nearby = []
    for property in Property.objects.all():
        if property.latitude and property.longitude:  # Ensure coordinates exist
            property_location = (property.latitude, property.longitude)
            distance = geodesic(user_location, property_location).km  # Calculate distance

            if distance <= radius_km:  # Check if within radius
                nearby.append({
                    "id": property.id,  # Ensure the property ID is included
                    "title": property.title,
                    "latitude": property.latitude,
                    "longitude": property.longitude,
                    "distance": round(distance, 2),
                })

    return render(request, "map.html", {"properties": nearby, "lat": user_location[0], "lon": user_location[1]})




from django.shortcuts import render, get_object_or_404
from property.models import Property  # Import your Property model

from django.shortcuts import render, get_object_or_404
from geopy.distance import geodesic
from django.utils.safestring import mark_safe
import json

from django.shortcuts import render, get_object_or_404
from geopy.distance import geodesic
from django.utils.safestring import mark_safe
import json

def test_map(request):
    # Fetch property with ID 1
    property = get_object_or_404(Property, id=18)

    mylat = property.latitude
    mylon = property.longitude
    
    user_location = (mylat, mylon)  # Fixed coordinates (change as needed)
    radius_km = 100  # Search radius

    nearby = []
    for property in Property.objects.all():
        if property.latitude and property.longitude:  # Ensure coordinates exist
            property_location = (property.latitude, property.longitude)
            distance = geodesic(user_location, property_location).km  # Calculate distance

            if distance <= radius_km:  # Check if within radius
                nearby.append({
                    "id": property.id,  # Ensure the property ID is included
                    "title": property.title,
                    "latitude": property.latitude,
                    "longitude": property.longitude,
                    "distance": round(distance, 2),
                })

    

    return render(request, "test/test_map.html", {
        "property": property,
        "properties": nearby, "lat": user_location[0], "lon": user_location[1]
    })


# views.py
from django.db.models import Q
from django.shortcuts import render
from property.models import Property
from django.core.paginator import Paginator
from geopy.distance import geodesic  # For calculating distances

def property_search(request):
    """
    View to handle property search with geolocation support.
    """
    query = request.GET.get('q', '')  # Get the search query from the URL parameter
    deal_type = request.GET.get('deal_type', '')  # Optional: Filter by deal type

    # Start with all published properties
    properties = Property.objects.filter(is_published=True)

    # Apply filters based on search query
    if query:
        try:
            # Check if the query contains latitude and longitude
            lat, lon = map(float, query.split(','))
            user_location = (lat, lon)
        except ValueError:
            # If not coordinates, treat it as a regular text query
            properties = properties.filter(
                Q(title__icontains=query) |
                Q(location__icontains=query) |
                Q(state__icontains=query) |
                Q(district__icontains=query) |
                Q(subdivision__icontains=query) |
                Q(village__icontains=query) |
                Q(pincode__icontains=query)
            )
        else:
            # If valid coordinates, filter properties within a certain radius
            nearby_properties = []
            for property in properties:
                if property.latitude and property.longitude:
                    property_location = (property.latitude, property.longitude)
                    distance = geodesic(user_location, property_location).kilometers
                    if distance <= 50:  # Filter properties within 50 km
                        property.distance = round(distance, 2)  # Add distance to the property object
                        nearby_properties.append(property)
            properties = nearby_properties

    # Apply additional filters if provided
    if deal_type:
        properties = properties.filter(deal_type=deal_type)

    # Paginate the results
    paginator = Paginator(properties, 10)  # Show 10 items per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'query': query,
        'deal_type': deal_type,
        'page_obj': page_obj,
    }

    return render(request, 'property_search.html', context)

from django.shortcuts import render
from django.db.models import Q
from geopy.distance import geodesic  # For distance calculation
from property.models import Property

def mysearch(request):
    state = request.GET.get('state', '')
    district = request.GET.get('district', '')
    subdivision = request.GET.get('subdivision', '')
    village = request.GET.get('village', '')
    deal_type = request.GET.get('deal_type', '')
    search_query = request.GET.get('search_query', '')

    user_lat = request.GET.get('latitude', None)
    user_lon = request.GET.get('longitude', None)

    properties = Property.objects.all()

    if state:
        properties = properties.filter(state__icontains=state)
    if district:
        properties = properties.filter(district__icontains=district)
    if subdivision:
        properties = properties.filter(subdivision__icontains=subdivision)
    if village:
        properties = properties.filter(village__icontains=village)
    if deal_type:
        properties = properties.filter(deal_type=deal_type)

    if search_query:
        properties = properties.filter(
            Q(state__icontains=search_query) |
            Q(district__icontains=search_query) |
            Q(subdivision__icontains=search_query) |
            Q(village__icontains=search_query) |
            Q(title__icontains=search_query) |
            Q(deal_type__icontains=search_query)
        )

    # Filter properties within a 50km radius if coordinates are provided
    if user_lat and user_lon:
        try:
            user_location = (float(user_lat), float(user_lon))
            nearby_properties = []
            
            for property in properties:
                if property.latitude and property.longitude:
                    property_location = (property.latitude, property.longitude)
                    distance = geodesic(user_location, property_location).km
                    
                    if distance <= 50:  # Only include properties within 50km
                        nearby_properties.append(property)
            
            properties = nearby_properties
        except ValueError:
            pass  # Handle invalid latitude/longitude values gracefully

    context = {
        'properties': properties,
        'search_query': search_query,
        'deal_type': deal_type,
    }

    return render(request, 'test/mysearch.html', context)


def service(request):
    return render(request, "service.html")

def contact(request):
    return render(request, "contact.html")
