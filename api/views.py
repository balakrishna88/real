# account/views.py

from django.shortcuts import render
from django.http import HttpResponse

# Login View
# account/views.py

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from api.forms import LandPropertyForm
from api.serializers import PropertySerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.http import HttpResponse

from property.models import CommercialProperty, IndustrialProperty, LandProperty, Property, PropertyActions, PropertyDocument, PropertyImage, PropertyUserTrack, PropertyVideo

# Login View (to render HTML page)
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            request.session['token'] = token.key  # Store token in session
            return render(request, 'api/login_success.html', {'token': token.key})

        return render(request, 'api/login.html', {'error': 'Invalid credentials'})

    return render(request, 'api/login.html')


# Create View (for signup)
# account/views.py
# account/views.py
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Create View (render HTML with auth status)
# views.py
def create_view(request):
    # Get the token from the session (if exists)
    token_key = request.session.get('token')
    auth_status = 'Not Authenticated'
    user = None  # Initialize user

    if token_key:
        try:
            # Attempt to retrieve the user using the token
            token = Token.objects.get(key=token_key)
            user = token.user
            auth_status = f'Authenticated as {user.username}'
        except Token.DoesNotExist:
            auth_status = 'Invalid or expired token'

    # Handle form submission if the request is POST
    if request.method == 'POST':
        property_form = LandPropertyForm(request.POST)
        images = request.FILES.getlist('images')  # Get multiple uploaded images
        documents = request.FILES.getlist('documents')  # Get multiple uploaded documents
        videos = request.FILES.getlist('videos')  # Get multiple uploaded videos

        if property_form.is_valid():
            # Save the property instance
            land_property = property_form.save(commit=False)
            land_property.user = user  # Associate the property with the authenticated user
            land_property.save()  # Save the property to the database

            # Save uploaded images associated with the property
            for image in images:
                PropertyImage.objects.create(property=land_property, image=image)

            # Save uploaded documents associated with the property
            for document in documents:
                PropertyDocument.objects.create(property=land_property, document=document)

            # Save uploaded videos associated with the property
            for video in videos:
                PropertyVideo.objects.create(property=land_property, video=video)

            return redirect('success')  # Redirect to a success page or another view
    else:
        property_form = LandPropertyForm()  # Empty form for GET request

    # Render the template with the form and authentication status
    return render(request, 'api/create.html', {
        'form': property_form,
        'auth_status': auth_status
    })




#--------------------

# Create View (render HTML with auth status)
# views.py
def LandProperty_create(request):
    # Get the token from the session (if exists)
    token_key = request.session.get('token')
    auth_status = 'Not Authenticated'
    user = None  # Initialize user

    if token_key:
        try:
            # Attempt to retrieve the user using the token
            token = Token.objects.get(key=token_key)
            user = token.user
            auth_status = f'Authenticated as {user.username}'
        except Token.DoesNotExist:
            auth_status = 'Invalid or expired token'

    # Handle form submission if the request is POST
    if request.method == 'POST':
        property_form = LandPropertyForm(request.POST)
        images = request.FILES.getlist('images')  # Get multiple uploaded images
        documents = request.FILES.getlist('documents')  # Get multiple uploaded documents
        videos = request.FILES.getlist('videos')  # Get multiple uploaded videos

        if property_form.is_valid():
            # Save the property instance
            land_property = property_form.save(commit=False)
            land_property.user = user  # Associate the property with the authenticated user
            land_property.save()  # Save the property to the database

            # Save uploaded images associated with the property
            for image in images:
                PropertyImage.objects.create(property=land_property, image=image)

            # Save uploaded documents associated with the property
            for document in documents:
                PropertyDocument.objects.create(property=land_property, document=document)

            # Save uploaded videos associated with the property
            for video in videos:
                PropertyVideo.objects.create(property=land_property, video=video)

            return redirect('success')  # Redirect to a success page or another view
    else:
        property_form = LandPropertyForm()  # Empty form for GET request

    # Render the template with the form and authentication status
    return render(request, 'api/LandProperty_create.html', {
        'form': property_form,
        'auth_status': auth_status
    })








# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from .forms import CommercialPropertyForm, IndustrialPropertyForm, ResidentialPropertyForm
from property.models import ResidentialProperty, PropertyImage, PropertyDocument, PropertyVideo

@login_required  # Ensure the user is logged in
def ResidentialProperty_create(request):
    # Get the token from the session
    token_key = request.session.get('token')
    auth_status = 'Not Authenticated'
    user = None

    if token_key:
        try:
            # Attempt to retrieve the user using the token
            token = Token.objects.get(key=token_key)
            user = token.user
            auth_status = f'Authenticated as {user.username}'
        except Token.DoesNotExist:
            auth_status = 'Invalid or expired token'

    # Handle form submission if the request is POST
    if request.method == 'POST':
        property_form = ResidentialPropertyForm(request.POST)
        images = request.FILES.getlist('images')  # Multiple uploaded images
        documents = request.FILES.getlist('documents')  # Multiple uploaded documents
        videos = request.FILES.getlist('videos')  # Multiple uploaded videos

        if property_form.is_valid():
            # Save the property instance
            residential_property = property_form.save(commit=False)
            residential_property.user = user  # Associate with the logged-in user
            residential_property.save()

            # Save uploaded images, documents, and videos
            for image in images:
                PropertyImage.objects.create(property=residential_property, image=image)

            for document in documents:
                PropertyDocument.objects.create(property=residential_property, document=document)

            for video in videos:
                PropertyVideo.objects.create(property=residential_property, video=video)

            return redirect('success')  # Redirect to a success page
    else:
        property_form = ResidentialPropertyForm()  # Empty form for GET request

    # Render the template with the form
    return render(request, 'api/ResidentialProperty_create.html', {
        'form': property_form,
        'auth_status': auth_status
    })





# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from .forms import ResidentialPropertyForm
from property.models import ResidentialProperty, PropertyImage, PropertyDocument, PropertyVideo

@login_required  # Ensure the user is logged in
def CommercialProperty_create(request):
    # Get the token from the session
    token_key = request.session.get('token')
    auth_status = 'Not Authenticated'
    user = None

    if token_key:
        try:
            # Attempt to retrieve the user using the token
            token = Token.objects.get(key=token_key)
            user = token.user
            auth_status = f'Authenticated as {user.username}'
        except Token.DoesNotExist:
            auth_status = 'Invalid or expired token'

    # Handle form submission if the request is POST
    if request.method == 'POST':
        property_form = CommercialPropertyForm(request.POST)
        images = request.FILES.getlist('images')  # Multiple uploaded images
        documents = request.FILES.getlist('documents')  # Multiple uploaded documents
        videos = request.FILES.getlist('videos')  # Multiple uploaded videos

        if property_form.is_valid():
            # Save the property instance
            residential_property = property_form.save(commit=False)
            residential_property.user = user  # Associate with the logged-in user
            residential_property.save()

            # Save uploaded images, documents, and videos
            for image in images:
                PropertyImage.objects.create(property=residential_property, image=image)

            for document in documents:
                PropertyDocument.objects.create(property=residential_property, document=document)

            for video in videos:
                PropertyVideo.objects.create(property=residential_property, video=video)

            return redirect('success')  # Redirect to a success page
    else:
        property_form = CommercialPropertyForm()  # Empty form for GET request

    # Render the template with the form
    return render(request, 'api/CommercialProperty_create.html', {
        'form': property_form,
        'auth_status': auth_status
    })







# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from .forms import ResidentialPropertyForm
from property.models import ResidentialProperty, PropertyImage, PropertyDocument, PropertyVideo

@login_required  # Ensure the user is logged in
def IndustrialProperty_create(request):
    # Get the token from the session
    token_key = request.session.get('token')
    auth_status = 'Not Authenticated'
    user = None

    if token_key:
        try:
            # Attempt to retrieve the user using the token
            token = Token.objects.get(key=token_key)
            user = token.user
            auth_status = f'Authenticated as {user.username}'
        except Token.DoesNotExist:
            auth_status = 'Invalid or expired token'

    # Handle form submission if the request is POST
    if request.method == 'POST':
        property_form = IndustrialPropertyForm(request.POST)
        images = request.FILES.getlist('images')  # Multiple uploaded images
        documents = request.FILES.getlist('documents')  # Multiple uploaded documents
        videos = request.FILES.getlist('videos')  # Multiple uploaded videos

        if property_form.is_valid():
            # Save the property instance
            residential_property = property_form.save(commit=False)
            residential_property.user = user  # Associate with the logged-in user
            residential_property.save()

            # Save uploaded images, documents, and videos
            for image in images:
                PropertyImage.objects.create(property=residential_property, image=image)

            for document in documents:
                PropertyDocument.objects.create(property=residential_property, document=document)

            for video in videos:
                PropertyVideo.objects.create(property=residential_property, video=video)

            return redirect('success')  # Redirect to a success page
    else:
        property_form = IndustrialPropertyForm()  # Empty form for GET request

    # Render the template with the form
    return render(request, 'api/IndustrialProperty_create.html', {
        'form': property_form,
        'auth_status': auth_status
    })

from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from property.models import Property, LandProperty, ResidentialProperty, CommercialProperty, IndustrialProperty


def property_detail(request, pk):
    # Fetch the property instance
    property = get_object_or_404(Property, pk=pk)

    # Initialize child model data
    land_property = None
    residential_property = None
    commercial_property = None
    industrial_property = None

    # Check the type of property and fetch the corresponding child model data
    if hasattr(property, 'landproperty'):
        land_property = LandProperty.objects.get(pk=property.pk)
    elif hasattr(property, 'residentialproperty'):
        residential_property = ResidentialProperty.objects.get(pk=property.pk)
    elif hasattr(property, 'commercialproperty'):
        commercial_property = CommercialProperty.objects.get(pk=property.pk)
    elif hasattr(property, 'industrialproperty'):
        industrial_property = IndustrialProperty.objects.get(pk=property.pk)

    # Pass the data to the template
    context = {
        'property': property,
        'land_property': land_property,
        'residential_property': residential_property,
        'commercial_property': commercial_property,
        'industrial_property': industrial_property,
    }

    return render(request, 'api/property_detail.html', context)




from django.shortcuts import render, get_object_or_404
from property.models import Property, LandProperty, ResidentialProperty, CommercialProperty, IndustrialProperty

def property_details_api(request, pk):
    # Fetch the property or return a 404 error
    property = get_object_or_404(Property, pk=pk)
    # Fetch comments for the property
    # Fetch all comments for the property (excluding replies)
    comments = Comment.objects.filter(property=property, parent__isnull=True).order_by('-created_at')

    # Initialize child model data
    land_property = None
    residential_property = None
    commercial_property = None
    industrial_property = None

    # Check the type of property and fetch the corresponding child model data
    if hasattr(property, 'landproperty'):
        land_property = LandProperty.objects.get(pk=property.pk)
    elif hasattr(property, 'residentialproperty'):
        residential_property = ResidentialProperty.objects.get(pk=property.pk)
    elif hasattr(property, 'commercialproperty'):
        commercial_property = CommercialProperty.objects.get(pk=property.pk)
    elif hasattr(property, 'industrialproperty'):
        industrial_property = IndustrialProperty.objects.get(pk=property.pk)

    # Track if the user has favorited the property
    is_favorite = False
    if request.user.is_authenticated:
        user_email = request.user.email
        user_track, _ = PropertyUserTrack.objects.get_or_create(user_email=user_email)
        is_favorite = property.id in user_track.property_favourite  # Check if property is in user's favorites

    # Fetch images, documents, and videos for the property
    images = PropertyImage.objects.filter(property=property)
    documents = PropertyDocument.objects.filter(property=property)
    videos = PropertyVideo.objects.filter(property=property)
    # Pass the data to the template
    context = {
        'property': property,
        'land_property': land_property,
        'residential_property': residential_property,
        'commercial_property': commercial_property,
        'industrial_property': industrial_property,
        'comments': comments,
        'images': images,  # Pass images to the template
        'documents': documents,  # Pass documents to the template
        'videos': videos,  # Pass videos to the template
        'is_favorite': is_favorite,
    }

    # Render the HTML template
    return render(request, 'api/api_property_details.html', context)




from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import View

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from property.models import Property, PropertyActions, PropertyUserTrack

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from property.models import Property, PropertyActions, PropertyUserTrack

class TrackLikeView(View):
    """
    A generic view to handle liking a property.
    Tracks activity for both authenticated users and guests.
    """

    def post(self, request, property_id, *args, **kwargs):
        # Fetch the property object
        property = get_object_or_404(Property, id=property_id)
        is_auth_user = request.user.is_authenticated

        # Update PropertyActions for global activity counts
        actions, _ = PropertyActions.objects.get_or_create(property=property)
        actions.update_count('likes', is_auth_user=is_auth_user, increment=True)

        # Update PropertyUserTrack for authenticated users
        if is_auth_user:
            user_email = request.user.email
            user_track, _ = PropertyUserTrack.objects.get_or_create(user_email=user_email)
            user_track.add_liked_property(property.id)

        # Redirect to the property detail page
        return HttpResponseRedirect(reverse('property-details-api', args=[property_id]))
    
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from property.models import Property, PropertyActions, PropertyUserTrack

class TrackUnlikeView(View):
    """
    A generic view to handle unliking a property.
    Tracks activity for authenticated users.
    """

    def post(self, request, property_id, *args, **kwargs):
        # Fetch the property object
        property = get_object_or_404(Property, id=property_id)
        is_auth_user = request.user.is_authenticated

        # Update PropertyActions for global activity counts
        actions, _ = PropertyActions.objects.get_or_create(property=property)
        actions.update_count('likes', is_auth_user=is_auth_user, increment=False)  # Decrement likes

        # Update PropertyUserTrack for authenticated users
        if is_auth_user:
            user_email = request.user.email
            user_track, _ = PropertyUserTrack.objects.get_or_create(user_email=user_email)
            user_track.remove_liked_property(property.id)  # Remove the property from liked list

        # Redirect to the property detail page
        return HttpResponseRedirect(reverse('property-details-api', args=[property_id]))



from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from property.models import Property, PropertyActions, PropertyUserTrack

class TrackViewView(View):
    """
    A generic view to handle tracking property views.
    Tracks activity for both authenticated users and guests.
    """

    def post(self, request, property_id, *args, **kwargs):
        # Fetch the property object
        property = get_object_or_404(Property, id=property_id)
        is_auth_user = request.user.is_authenticated

        # Update PropertyActions for global activity counts
        actions, _ = PropertyActions.objects.get_or_create(property=property)
        actions.update_count('views', is_auth_user=is_auth_user, increment=True)

        # Update PropertyUserTrack for authenticated users
        if is_auth_user:
            user_email = request.user.email
            user_track, _ = PropertyUserTrack.objects.get_or_create(user_email=user_email)
            user_track.add_viewed_property(property.id)

        # Redirect to the property detail page
        return HttpResponseRedirect(reverse('property-details-api', args=[property_id]))

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from property.models import Property, PropertyActions, PropertyUserTrack

class TrackActionView(View):
    """
    A generic view to handle actions on a property (like, dislike, share, etc.).
    """

    def post(self, request, property_id, action_type, *args, **kwargs):
        property = get_object_or_404(Property, id=property_id)
        is_auth_user = request.user.is_authenticated

        # Update PropertyActions for global activity counts
        actions, _ = PropertyActions.objects.get_or_create(property=property)
        actions.update_count(action_type, is_auth_user=is_auth_user, increment=True)

        # Update PropertyUserTrack for authenticated users
        if is_auth_user:
            user_email = request.user.email
            user_track, _ = PropertyUserTrack.objects.get_or_create(user_email=user_email)
            if action_type == "likes":
                user_track.add_liked_property(property.id)
            elif action_type == "dislikes":
                user_track.remove_liked_property(property.id)
            elif action_type == "shares":
                user_track.add_shared_property(property.id)  # Handle "Share" action
            elif action_type == "views":
                user_track.add_viewed_property(property.id)
            elif action_type == "comments":
                user_track.add_commented_property(property.id)
            elif action_type == "reports":
                user_track.add_reported_property(property.id)
            elif action_type == "favourites":
                user_track.add_favourite_property(property.id)

        # Redirect to the property detail page
        return HttpResponseRedirect(reverse('property-details-api', args=[property_id]))


from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from property.models import Property, PropertyActions, PropertyUserTrack

class TrackFavoriteView(View):
    """
    A generic view to handle favoriting a property.
    Tracks activity for authenticated users.
    """

    def post(self, request, property_id, *args, **kwargs):
        # Fetch the property object
        property = get_object_or_404(Property, id=property_id)
        is_auth_user = request.user.is_authenticated

        # Update PropertyActions for global activity counts
        actions, _ = PropertyActions.objects.get_or_create(property=property)
        actions.update_count('favourites', is_auth_user=is_auth_user, increment=True)  # Increment favorites

        # Update PropertyUserTrack for authenticated users
        if is_auth_user:
            user_email = request.user.email
            user_track, _ = PropertyUserTrack.objects.get_or_create(user_email=user_email)
            user_track.add_favourite_property(property.id)  # Add the property to favorites

        # Redirect to the property detail page
        return HttpResponseRedirect(reverse('property-details-api', args=[property_id]))


class TrackUnfavoriteView(View):
    """
    A generic view to handle unfavoriting a property.
    Tracks activity for authenticated users.
    """

    def post(self, request, property_id, *args, **kwargs):
        # Fetch the property object
        property = get_object_or_404(Property, id=property_id)
        is_auth_user = request.user.is_authenticated

        # Update PropertyActions for global activity counts
        actions, _ = PropertyActions.objects.get_or_create(property=property)
        actions.update_count('favourites', is_auth_user=is_auth_user, increment=False)  # Decrement favorites

        # Update PropertyUserTrack for authenticated users
        if is_auth_user:
            user_email = request.user.email
            user_track, _ = PropertyUserTrack.objects.get_or_create(user_email=user_email)
            user_track.remove_favourite_property(property.id)  # Remove the property from favorites

        # Redirect to the property detail page
        return HttpResponseRedirect(reverse('property-details-api', args=[property_id]))



from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from django.contrib import messages
from property.models import Property, PropertyActions, PropertyUserTrack, Report

class TrackReportView(View):
    """
    A generic view to handle reporting a property.
    Tracks activity for both authenticated users and guests.
    """

    def post(self, request, property_id, *args, **kwargs):
        # Fetch the property object
        property_instance = get_object_or_404(Property, id=property_id)
        report_type = request.POST.get('report_type')
        additional_info = request.POST.get('additional_info', '')

        # Validate the report type
        if report_type not in dict(Report.REPORT_CHOICES).keys():
            messages.error(request, "Invalid report type.")
            return HttpResponseRedirect(reverse('property-details-api', args=[property_id]))

        # Determine the user value
        user = request.user.username if request.user.is_authenticated else "guest"

        # Create the report
        report = Report.objects.create(
            post=property_instance,  # Use 'post' to match the field in the Report model
            user=user,  # Store "guest" directly for unauthenticated users
            report_type=report_type,
            additional_info=additional_info
        )

        # Update PropertyActions for reports
        actions, _ = PropertyActions.objects.get_or_create(property=property_instance)
        actions.update_count('reports', is_auth_user=request.user.is_authenticated, increment=True)

        # Update PropertyUserTrack for authenticated users
        if request.user.is_authenticated:
            user_email = request.user.email
            user_track, _ = PropertyUserTrack.objects.get_or_create(user_email=user_email)
            user_track.add_reported_property(property_instance.id)

        # Add a success message
        messages.success(request, "Thank you for reporting this property. We will review it shortly.")

        # Redirect to the property detail page
        return HttpResponseRedirect(reverse('property-details-api', args=[property_id]))




from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from property.models import Property, Comment, PropertyActions, PropertyUserTrack

class TrackCommentView(View):
    """
    A generic view to handle adding a comment to a property.
    """

    def post(self, request, property_id, *args, **kwargs):
        # Fetch the property object
        property = get_object_or_404(Property, id=property_id)
        content = request.POST.get('content')
        is_auth_user = request.user.is_authenticated

        # Create the comment
        comment = Comment.objects.create(
            property=property,
            user=request.user.username if is_auth_user else "guest",
            content=content
        )

        # Update PropertyActions for global activity counts
        actions, _ = PropertyActions.objects.get_or_create(property=property)
        actions.update_count('comments', is_auth_user=is_auth_user, increment=True)

        # Update PropertyUserTrack for authenticated users
        if is_auth_user:
            user_email = request.user.email
            user_track, _ = PropertyUserTrack.objects.get_or_create(user_email=user_email)
            user_track.add_commented_property(property.id)

        # Redirect to the property detail page
        return HttpResponseRedirect(reverse('property-details-api', args=[property_id]))
    

class TrackCommentReplyView(View):
    """
    A generic view to handle adding a reply to a comment on a property.
    """

    def post(self, request, property_id, parent_id, *args, **kwargs):
        # Fetch the property and parent comment
        property = get_object_or_404(Property, id=property_id)
        parent_comment = get_object_or_404(Comment, id=parent_id)
        content = request.POST.get('content')
        is_auth_user = request.user.is_authenticated

        # Create the reply
        reply = Comment.objects.create(
            property=property,
            parent=parent_comment,
            user=request.user.username if is_auth_user else "guest",
            content=content
        )

        # Update PropertyActions for global activity counts
        actions, _ = PropertyActions.objects.get_or_create(property=property)
        actions.update_count('comments', is_auth_user=is_auth_user, increment=True)

        # Update PropertyUserTrack for authenticated users
        if is_auth_user:
            user_email = request.user.email
            user_track, _ = PropertyUserTrack.objects.get_or_create(user_email=user_email)
            user_track.add_commented_property(property.id)

        # Redirect to the property detail page
        return HttpResponseRedirect(reverse('property-details-api', args=[property_id]))
    

class TrackDeleteCommentView(View):
    """
    A generic view to handle deleting a comment or reply on a property.
    """

    def post(self, request, comment_id, *args, **kwargs):
        # Fetch the comment
        comment = get_object_or_404(Comment, id=comment_id)
        property_id = comment.property.id
        is_auth_user = request.user.is_authenticated

        # Check if the comment belongs to the logged-in user or the author of the property
        if request.user.username == comment.user or request.user == comment.property.author:
            comment.delete()

            # Update PropertyActions for global activity counts
            actions, _ = PropertyActions.objects.get_or_create(property=comment.property)
            actions.update_count('comments', is_auth_user=is_auth_user, increment=False)

            # Update PropertyUserTrack for authenticated users
            if is_auth_user:
                user_email = request.user.email
                user_track, _ = PropertyUserTrack.objects.get_or_create(user_email=user_email)
                if property_id in user_track.property_comment:
                    user_track.property_comment.remove(property_id)
                    user_track.save()

        # Redirect to the property detail page
        return HttpResponseRedirect(reverse('property-details-api', args=[property_id]))
    


#--------------------

# account/views.py

from django.contrib.auth import logout
from django.http import JsonResponse

# Logout View: Clears session and logs out the user
def logout_view(request):
    # Clear the session and remove the token
    request.session.flush()  # This will clear all session data, including the token
    logout(request)  # This will log out the user (if they were authenticated)

    # Redirect to a page or return a response indicating successful logout
    return JsonResponse({'message': 'You have been logged out successfully.'}, status=200)


# views.py

def success(request):
    return render(request, 'api/success.html')

def home(request):
    return render(request, 'api/home.html')




from django.shortcuts import render
import requests

def get_location(request):
    latitude = None
    longitude = None
    address = None
    error_message = None

    if request.method == "POST":
        # Get the address from the form
        address = request.POST.get("address")
        
        if address:
            # OpenCage API key (Replace with your OpenCage API key)
            API_KEY = "676b45079f5d4134a3a3f97cf15b481a"
            
            # OpenCage API URL
            url = "https://api.opencagedata.com/geocode/v1/json"
            
            # Parameters for the request
            params = {
                'q': address,  # The address provided by the user
                'key': API_KEY  # Your OpenCage API key
            }
            
            # Sending a request to OpenCage API
            response = requests.get(url, params=params)
            data = response.json()

            # Check if the response contains results
            if data['status']['code'] == 200 and data['results']:
                # Extract latitude and longitude from the first result
                latitude = data['results'][0]['geometry']['lat']
                longitude = data['results'][0]['geometry']['lng']
            else:
                error_message = "Could not find the location. Please try again with a different address."

    return render(
        request,
        "api/location.html",
        {
            "latitude": latitude,
            "longitude": longitude,
            "address": address,
            "error_message": error_message
        }
    )




import requests
from django.http import JsonResponse

def get_coordinates(request):
    short_url = request.GET.get('url', '')

    if not short_url:
        return JsonResponse({'error': 'No URL provided'}, status=400)

    try:
        # Step 1: Expand the short URL
        response = requests.get(short_url, allow_redirects=True)
        full_url = response.url
        print("Full URL:", full_url)  # Debugging: Print the expanded URL

        # Step 2: Extract coordinates from the URL
        if 'search/' in full_url:
            # Extract the part after 'search/' and before '?'
            search_part = full_url.split('search/')[1].split('?')[0]
            if ',' in search_part:
                latitude, longitude = search_part.split(',')[:2]
                return JsonResponse({'latitude': latitude, 'longitude': longitude})
        elif '@' in full_url:
            # Extract the part after '@' and before '/'
            coordinates_part = full_url.split('@')[1].split('/')[0]
            latitude, longitude = coordinates_part.split(',')[:2]
            return JsonResponse({'latitude': latitude, 'longitude': longitude})
        elif '!3d' in full_url and '!4d' in full_url:
            # Extract coordinates from the !3d and !4d parameters
            latitude = full_url.split('!3d')[1].split('!')[0]
            longitude = full_url.split('!4d')[1].split('!')[0]
            return JsonResponse({'latitude': latitude, 'longitude': longitude})
        else:
            return JsonResponse({'error': 'Coordinates not found in URL'}, status=404)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)