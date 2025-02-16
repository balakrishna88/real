import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import CommercialProperty, IndustrialProperty, LandProperty, Property, PropertyImage, PropertyDocument, PropertyVideo, PropertyUserTrack, ResidentialProperty
from .forms import LandPropertyForm, PropertyImageForm, PropertyDocumentForm, PropertyVideoForm



from django.shortcuts import render, redirect
from .forms import (
    LandPropertyForm,
    ResidentialPropertyForm,
    CommercialPropertyForm,
    IndustrialPropertyForm,
    PropertyImageForm,
    PropertyDocumentForm,
    PropertyVideoForm,
)
from .models import PropertyImage, PropertyDocument, PropertyVideo


def create_index(request):
    # Initialize all forms
    l_form = LandPropertyForm()
    r_form = ResidentialPropertyForm()
    c_form = CommercialPropertyForm()
    i_form = IndustrialPropertyForm()
    image_form = PropertyImageForm()
    document_form = PropertyDocumentForm()
    video_form = PropertyVideoForm()

    if request.method == 'POST':
        if 'land_property_form' in request.POST:  # Handle LandProperty form submission
            l_form = LandPropertyForm(request.POST)
            image_form = PropertyImageForm(request.POST, request.FILES)
            document_form = PropertyDocumentForm(request.POST, request.FILES)
            video_form = PropertyVideoForm(request.POST, request.FILES)

            if l_form.is_valid():
                land_property = l_form.save(commit=False)
                land_property.user = request.user
                land_property.save()

                # Handle file uploads
                for image in request.FILES.getlist('images'):
                    PropertyImage.objects.create(property=land_property, image=image)

                for document in request.FILES.getlist('documents'):
                    PropertyDocument.objects.create(property=land_property, document=document)

                for video in request.FILES.getlist('videos'):
                    PropertyVideo.objects.create(property=land_property, video=video)

                messages.success(request, 'Land property created successfully!')
                return redirect('success_page')
            else:
                # Log or print form errors for debugging
                print("LandPropertyForm errors:", l_form.errors)
                print("PropertyImageForm errors:", image_form.errors)
                print("PropertyDocumentForm errors:", document_form.errors)
                print("PropertyVideoForm errors:", video_form.errors)

                # Add error messages to the user
                messages.error(request, 'There was an error with your submission. Please check the form.')

        elif 'residential_property_form' in request.POST:  # Handle ResidentialProperty form submission
            r_form = ResidentialPropertyForm(request.POST)
            image_form = PropertyImageForm(request.POST, request.FILES)
            document_form = PropertyDocumentForm(request.POST, request.FILES)
            video_form = PropertyVideoForm(request.POST, request.FILES)
            if r_form.is_valid():
                residential_property = r_form.save(commit=False)
                residential_property.user = request.user
                residential_property.save()

                # Handle file uploads
                for image in request.FILES.getlist('images'):
                    PropertyImage.objects.create(property=residential_property, image=image)

                for document in request.FILES.getlist('documents'):
                    PropertyDocument.objects.create(property=residential_property, document=document)

                for video in request.FILES.getlist('videos'):
                    PropertyVideo.objects.create(property=residential_property, video=video)

                return redirect('success_page')  # Redirect to a success page
            
            else:
                # Log or print form errors for debugging
                print("ResidentialPropertyForm errors:", r_form.errors)
                print("PropertyImageForm errors:", image_form.errors)
                print("PropertyDocumentForm errors:", document_form.errors)
                print("PropertyVideoForm errors:", video_form.errors)

                # Add error messages to the user
                messages.error(request, 'There was an error with your submission. Please check the form.')

        elif 'commercial_property_form' in request.POST:  # Handle CommercialProperty form submission
            c_form = CommercialPropertyForm(request.POST)
            image_form = PropertyImageForm(request.POST, request.FILES)
            document_form = PropertyDocumentForm(request.POST, request.FILES)
            video_form = PropertyVideoForm(request.POST, request.FILES)
            if c_form.is_valid():
                commercial_property = c_form.save(commit=False)
                commercial_property.user = request.user
                commercial_property.save()

                # Handle file uploads
                for image in request.FILES.getlist('images'):
                    PropertyImage.objects.create(property=commercial_property, image=image)

                for document in request.FILES.getlist('documents'):
                    PropertyDocument.objects.create(property=commercial_property, document=document)

                for video in request.FILES.getlist('videos'):
                    PropertyVideo.objects.create(property=commercial_property, video=video)

                return redirect('success_page')  # Redirect to a success page
            
            else:
                # Log or print form errors for debugging
                print("CommercialPropertyForm errors:", c_form.errors)
                print("PropertyImageForm errors:", image_form.errors)
                print("PropertyDocumentForm errors:", document_form.errors)
                print("PropertyVideoForm errors:", video_form.errors)

        elif 'industrial_property_form' in request.POST:  # Handle IndustrialProperty form submission
            i_form = IndustrialPropertyForm(request.POST)
            image_form = PropertyImageForm(request.POST, request.FILES)
            document_form = PropertyDocumentForm(request.POST, request.FILES)
            video_form = PropertyVideoForm(request.POST, request.FILES)
            if i_form.is_valid():
                industrial_property = i_form.save(commit=False)
                industrial_property.user = request.user
                industrial_property.save()

                # Handle file uploads
                for image in request.FILES.getlist('images'):
                    PropertyImage.objects.create(property=industrial_property, image=image)

                for document in request.FILES.getlist('documents'):
                    PropertyDocument.objects.create(property=industrial_property, document=document)

                for video in request.FILES.getlist('videos'):
                    PropertyVideo.objects.create(property=industrial_property, video=video)

                return redirect('success_page')  # Redirect to a success page
            else:
                # Log or print form errors for debugging
                print("IndustrialPropertyForm errors:", c_form.errors)
                print("PropertyImageForm errors:", image_form.errors)
                print("PropertyDocumentForm errors:", document_form.errors)
                print("PropertyVideoForm errors:", video_form.errors)

    # Pass forms to the template
    context = {
        'page_title': 'Property Creation Index',
        'description': 'Choose between Land, Residential, Commercial, and Industrial property creation.',
        'l_form': l_form,  # LandProperty form
        'r_form': r_form,  # ResidentialProperty form
        'c_form': c_form,  # CommercialProperty form
        'i_form': i_form,  # IndustrialProperty form
        'image_form': image_form,  # Image upload form
        'document_form': document_form,  # Document upload form
        'video_form': video_form,  # Video upload form
    }

    return render(request, 'property/create/index.html', context)






def test(request):
    return render(request, 'property/create/test.html')



# property/views.py
from django.shortcuts import render

def success_page(request):
    return render(request, 'property/create/success.html')

# View to edit an existing property
@login_required  # Ensure the user is logged in
def edit_property(request, property_id):
    # Fetch the property by its ID, or return 404 if not found
    property_instance = get_object_or_404(Property, id=property_id, user=request.user)

    if request.method == 'POST':
        # Initialize the forms with the existing data
        property_form = LandPropertyForm(request.POST, instance=property_instance)
        image_form = PropertyImageForm(request.POST, request.FILES)
        document_form = PropertyDocumentForm(request.POST, request.FILES)
        video_form = PropertyVideoForm(request.POST, request.FILES)

        # If all forms are valid, update the property and its associated files
        if property_form.is_valid() and image_form.is_valid() and document_form.is_valid() and video_form.is_valid():
            property_instance = property_form.save(commit=False)
            property_instance.user = request.user  # Ensure user is set correctly
            property_instance.save()

            # Update the images, documents, and videos if provided
            for image in request.FILES.getlist('images'):
                PropertyImage.objects.create(property=property_instance, image=image)
            for document in request.FILES.getlist('documents'):
                PropertyDocument.objects.create(property=property_instance, document=document)
            for video in request.FILES.getlist('videos'):
                PropertyVideo.objects.create(property=property_instance, video=video)

            # Redirect to the property detail page after saving
            return redirect('property_detail', property_id=property_instance.id)

    else:
        # Initialize forms with existing data on GET request
        property_form = LandPropertyForm(instance=property_instance)
        image_form = PropertyImageForm()
        document_form = PropertyDocumentForm()
        video_form = PropertyVideoForm()

    # Fetch existing files associated with the property
    existing_images = PropertyImage.objects.filter(property=property_instance)
    existing_documents = PropertyDocument.objects.filter(property=property_instance)
    existing_videos = PropertyVideo.objects.filter(property=property_instance)

    # Render the property edit template
    return render(request, 'property/edit_property.html', {
        'property_form': property_form,
        'image_form': image_form,
        'document_form': document_form,
        'video_form': video_form,
        'property_instance': property_instance,  # Pass the property to the template
        'existing_images': existing_images,
        'existing_documents': existing_documents,
        'existing_videos': existing_videos,
    })


# View to delete property files (images, documents, or videos)
@login_required
def delete_property_file(request, file_id, file_type):
    # Determine which model to delete based on the file type
    if file_type == 'image':
        file_instance = get_object_or_404(PropertyImage, id=file_id, property__user=request.user)
    elif file_type == 'document':
        file_instance = get_object_or_404(PropertyDocument, id=file_id, property__user=request.user)
    elif file_type == 'video':
        file_instance = get_object_or_404(PropertyVideo, id=file_id, property__user=request.user)
    else:
        return redirect('edit_property', property_id=file_id)  # If invalid file_type, redirect to edit property

    # Delete the file instance
    file_instance.delete()

    # Redirect back to the property edit page after deletion
    return redirect('edit_property', property_id=file_instance.property.id)


# View to display the details of a property
from django.shortcuts import render, get_object_or_404
from .models import Property, PropertyUserTrack, PropertyActions
from geopy.distance import geodesic

def property_detail(request, property_slug):
    # Fetch the property instance
    property_instance = get_object_or_404(Property, slug=property_slug)
    activity_data = get_property_activity(property_instance.id)

    mylat = property_instance.latitude
    mylon = property_instance.longitude
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
                    "slug": property.slug,
                    "title": property.title,
                    "latitude": property.latitude,
                    "longitude": property.longitude,
                    "distance": round(distance, 2),
                })
   

    
    
    author = property_instance.user 

    # Fetch images related to the property
    images = property_instance.images.all()

    # Fetch comments (top-level) and replies associated with the property
    comments = property_instance.propertycomments.filter(parent__isnull=True).order_by('-created_at')
    replies = property_instance.propertycomments.filter(parent__isnull=False).order_by('-created_at')

    # Track favorite and like status
    is_favorite = False
    is_like = False

    # Get or create PropertyActions for tracking views
    property_actions, _ = PropertyActions.objects.get_or_create(property=property_instance)

    user_phone_number = None

    if request.user.is_authenticated:
        # Authenticated user tracking
        user_email = request.user.email
        user_track, _ = PropertyUserTrack.objects.get_or_create(user_email=user_email)
        user_phone_number = request.user.phone_number

        is_favorite = property_instance.id in user_track.property_favourite
        is_like = property_instance.id in user_track.property_like

        # Track views for authenticated users
        if property_instance.id not in user_track.property_view:
            user_track.property_view.append(property_instance.id)
            user_track.save()

            # Increment authenticated views
            property_actions.update_count("views", is_auth_user=True)

    else:
        # Guest user tracking using session
        viewed_properties = request.session.get('viewed_properties', [])

        if property_instance.id not in viewed_properties:
            viewed_properties.append(property_instance.id)
            request.session['viewed_properties'] = viewed_properties  # Store in session
            request.session.modified = True  # Ensure session is saved

            # Increment guest views
            property_actions.update_count("views", is_auth_user=False)

    # Fetch 6 random properties
    random_posts = Property.objects.order_by('?')[:6]

    # Render the template
    return render(request, 'property/property_detail.html', {
        'property': property_instance,
        'images': images,
        'comments': comments,
        'replies': replies,
        'is_favorite': is_favorite,
        'is_like': is_like,
        'random_posts': random_posts,
        "author": author,
        'user_phone_number': user_phone_number,
        "properties": nearby, "lat": user_location[0], "lon": user_location[1],
        'activity_data': activity_data,

    })



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from chat.models import Room
from account.models import Account  # Import your custom Account model

@login_required
def chat_with_author(request, author_id):
    user = request.user
    author = get_object_or_404(Account, id=author_id)

    if user == author:
        return redirect("home")  # Prevent chatting with self

    # Generate a unique room name based on user and author IDs
    room_name = f"chat-{min(user.id, author.id)}-{max(user.id, author.id)}"
    room_slug = slugify(room_name)

    # Find or create the chat room
    room, created = Room.objects.get_or_create(slug=room_slug, defaults={"name": room_name})
    
    # Ensure both users are participants
    room.participants.add(user, author)

    # Redirect to the room detail page using its ID
    return redirect("room_detail", id=room.id)




from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from chat.models import Notification
from account.models import Account  

def request_mobile(request):
    if request.method == "POST":
        # Get form data
        user_id = request.POST.get("user_id")
        message = request.POST.get("message", "I would like to request your mobile number.")
        phone_number = request.POST.get("phone_number", "").strip()  # Get user input phone number

        # Ensure a user exists
        user = get_object_or_404(Account, id=user_id)

        # If the authenticated user has a stored phone number, use it
        if request.user.is_authenticated and request.user.phone_number:
            phone_number = request.user.phone_number  

        # Create the notification
        Notification.objects.create(
            user=user,
            message=f"{message}\nRequested by: {request.user.email}\nPhone: {phone_number}",
            notification_type=Notification.MOBILE_REQUEST,
            is_read=False,
        )

        # Success message
        messages.success(request, "Mobile request sent successfully.")
        return redirect(request.META.get("HTTP_REFERER", "home"))

    # Redirect to home if accessed directly
    return redirect("home")



#section 2


# realpost/views.py
from django.shortcuts import get_object_or_404, redirect
from .models import Property, PropertyActions, PropertyUserTrack

def track_like(request, property_id):
    """
    View to handle liking a property.
    Tracks activity for both authenticated users and guests.
    """
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

    # Redirect back to the property details page
    return redirect('property_detail', property_slug=property.slug)



from django.shortcuts import get_object_or_404, redirect
from .models import Property, PropertyActions, PropertyUserTrack

from django.shortcuts import get_object_or_404, redirect
from .models import Property, PropertyActions, PropertyUserTrack

def track_unlike(request, property_id):
    """
    View to handle unliking a property.
    """
    property_obj = get_object_or_404(Property, id=property_id)

    if request.user.is_authenticated:
        user_email = request.user.email
        user_track = PropertyUserTrack.objects.filter(user_email=user_email).first()

        # Remove the property from the user's liked properties
        if user_track:
            user_track.remove_liked_property(property_obj.id)

        # Decrement the like count in PropertyActions
        actions, _ = PropertyActions.objects.get_or_create(property=property_obj)
        actions.update_count('likes', is_auth_user=True, increment=False)

    # Redirect back to the property details page using slug
    return redirect('property_detail', property_slug=property_obj.slug)



# views.py
from django.shortcuts import get_object_or_404, redirect
from .models import Property, PropertyActions, PropertyUserTrack

def track_share(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    is_auth_user = request.user.is_authenticated

    # Update PropertyActions (share count)
    actions, _ = PropertyActions.objects.get_or_create(property=property)
    actions.update_count('shares', is_auth_user=is_auth_user, increment=True)

    # Update PropertyUserTrack for authenticated users
    if is_auth_user:
        user_email = request.user.email
        user_track, _ = PropertyUserTrack.objects.get_or_create(user_email=user_email)
        user_track.add_shared_property(property.id)

    return redirect('property_detail', property_slug=property.slug)



# views.py
from django.shortcuts import get_object_or_404, redirect
from .models import Property, PropertyActions, PropertyUserTrack

def track_view(request, property_id):
    """
    View to track when a property is viewed.
    Updates PropertyActions for overall views and PropertyUserTrack for authenticated users.
    """
    property = get_object_or_404(Property, id=property_id)
    is_auth_user = request.user.is_authenticated

    # Update PropertyActions for overall views
    actions, _ = PropertyActions.objects.get_or_create(property=property)
    actions.update_count('views', is_auth_user=is_auth_user, increment=True)

    # Update PropertyUserTrack for authenticated users
    if is_auth_user:
        user_email = request.user.email
        user_track, _ = PropertyUserTrack.objects.get_or_create(user_email=user_email)
        user_track.add_viewed_property(property.id)

    return redirect('property_detail', property_id=property_id)



from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Property, PropertyActions, PropertyUserTrack, Report

def track_report(request, property_id):
    """
    View to handle reporting a property.
    Reports are saved and activity counts are updated for the property.
    """
    if request.method == "POST":
        property_instance = get_object_or_404(Property, id=property_id)
        report_type = request.POST.get('report_type')
        additional_info = request.POST.get('additional_info', '')

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

        messages.success(request, "Thank you for reporting this property. We will review it shortly.")

    return redirect('property_detail', property_slug=property_instance.slug)






from django.shortcuts import redirect, get_object_or_404
from .models import Property, Comment, PropertyActions, PropertyUserTrack

def property_comment(request, property_id):
    """
    Handle adding a comment to a property.
    """
    if request.method == "POST":
        content = request.POST.get('content')
        property = get_object_or_404(Property, id=property_id)
        comment = Comment.objects.create(
            property=property, 
            user=request.user.username if request.user.is_authenticated else "guest", 
            content=content
        )
        
        # Update PropertyActions
        actions, _ = PropertyActions.objects.get_or_create(property=property)
        actions.update_count('comments', is_auth_user=request.user.is_authenticated, increment=True)

        # Update PropertyUserTrack for authenticated users
        if request.user.is_authenticated:
            user_email = request.user.email
            user_track, _ = PropertyUserTrack.objects.get_or_create(user_email=user_email)
            user_track.add_commented_property(property.id)

    return redirect('property_detail', property_slug=property.slug)

def property_comment_reply(request, property_id, parent_id):
    """
    Handle adding a reply to a comment on a property.
    """
    if request.method == "POST":
        content = request.POST.get('content')
        property = get_object_or_404(Property, id=property_id)
        parent_comment = get_object_or_404(Comment, id=parent_id)
        reply = Comment.objects.create(
            property=property, 
            parent=parent_comment, 
            user=request.user.username if request.user.is_authenticated else "guest", 
            content=content
        )
        
        # Update PropertyActions
        actions, _ = PropertyActions.objects.get_or_create(property=property)
        actions.update_count('comments', is_auth_user=request.user.is_authenticated, increment=True)

        # Update PropertyUserTrack for authenticated users
        if request.user.is_authenticated:
            user_email = request.user.email
            user_track, _ = PropertyUserTrack.objects.get_or_create(user_email=user_email)
            user_track.add_commented_property(property.id)

    return redirect('property_detail', property_slug=property.slug)

from django.shortcuts import get_object_or_404, redirect
from .models import Comment, PropertyActions, PropertyUserTrack

def delete_property_comment(request, comment_id):
    """
    Handle deleting a comment or reply on a property.
    """
    comment = get_object_or_404(Comment, id=comment_id)

    # Check if the comment belongs to the logged-in user or the author of the property
    if request.user.username == comment.user or request.user == comment.property.author:
        property = comment.property  # Access the property associated with the comment
        property_id = property.id

        # Delete the comment
        comment.delete()
        
        # Update PropertyActions
        actions, _ = PropertyActions.objects.get_or_create(property=property)
        actions.update_count('comments', is_auth_user=request.user.is_authenticated, increment=False)

        # Update PropertyUserTrack for authenticated users
        if request.user.is_authenticated:
            user_email = request.user.email
            user_track, _ = PropertyUserTrack.objects.get_or_create(user_email=user_email)
            if property_id in user_track.property_comment:
                user_track.property_comment.remove(property_id)
                user_track.save()
    
    # Redirect to the property detail page
    return redirect('property_detail', property_slug=property.slug)


from django.shortcuts import get_object_or_404, redirect
from .models import Property, PropertyActions, PropertyUserTrack

def add_favourite(request, property_id):
    """
    View to add a property to the favorites list for the authenticated user.
    """
    property = get_object_or_404(Property, id=property_id)
    if request.user.is_authenticated:
        user_email = request.user.email
        user_track, _ = PropertyUserTrack.objects.get_or_create(user_email=user_email)
        user_track.add_favourite_property(property_id)

        # Update the global favorite count
        actions, _ = PropertyActions.objects.get_or_create(property=property)
        actions.update_count('favourites', is_auth_user=True, increment=True)

    return redirect('property_detail', property_slug=property.slug)



def remove_favourite(request, property_id):
    """
    View to remove a property from the favorites list for the authenticated user.
    """
    property = get_object_or_404(Property, id=property_id)
    if request.user.is_authenticated:
        user_email = request.user.email
        user_track = PropertyUserTrack.objects.filter(user_email=user_email).first()
        if user_track:
            user_track.remove_favourite_property(property_id)

            # Update the global favorite count
            actions, _ = PropertyActions.objects.get_or_create(property=property)
            actions.update_count('favourites', is_auth_user=True, increment=False)

    return redirect('property_detail', property_slug=property.slug)







#section 3 




# utils.py
from django.core.paginator import Paginator

# utils.py
from django.core.paginator import Paginator

# utils.py
from django.core.paginator import Paginator

def paginate_queryset(request, queryset, items_per_page=10):
    """
    Utility function to paginate a queryset.
    
    Args:
        request: The HTTP request object.
        queryset: The queryset to paginate.
        items_per_page: Number of items per page (default is 10).
    
    Returns:
        A Page object representing the current page.
    """
    paginator = Paginator(queryset, items_per_page)
    page_number = request.GET.get('page', 1)  # Default to page 1 if no page is specified
    return paginator.get_page(page_number)

# views.py
from django.shortcuts import render
from .models import LandProperty, ResidentialProperty, CommercialProperty, IndustrialProperty, Property


def property_list(request, property_type=None):
    """
    View to display paginated lists of properties based on the property type.
    """
    # Determine the queryset based on the property type
    if property_type == 'land':
        queryset = LandProperty.objects.filter(is_published=True).order_by('-listing_date')
    elif property_type == 'residential':
        queryset = ResidentialProperty.objects.filter(is_published=True).order_by('-listing_date')
    elif property_type == 'commercial':
        queryset = CommercialProperty.objects.filter(is_published=True).order_by('-listing_date')
    elif property_type == 'industrial':
        queryset = IndustrialProperty.objects.filter(is_published=True).order_by('-listing_date')
    else:
        queryset = Property.objects.filter(is_published=True).order_by('-listing_date')

    # Use the pagination utility function
    page_obj = paginate_queryset(request, queryset, items_per_page=10)
    # Fetch activity data for each property in the paginated queryset
    properties_with_activity = []
    for property in page_obj:
        activity_data = get_property_activity(property.id)
        property.total_views = activity_data["views"]  # Attach views to the property object
        property.total_likes = activity_data["likes"]  # Attach likes to the property object
        property.total_shares = activity_data["shares"]  # Attach shares to the property object
        properties_with_activity.append(property)
    

    context = {
        'page_obj': page_obj,
        'property_type': property_type,
        
    }

    return render(request, 'property/property_list.html', context)


# views.py
from django.shortcuts import render
from .models import LandProperty, ResidentialProperty, CommercialProperty, IndustrialProperty, Property

def property_index(request):
    """
    View to display a limited number of properties for each type on the index page.
    """
    # Fetch only 6 objects for each property type
    land_properties = LandProperty.objects.filter(is_published=True).order_by('-listing_date')[:6]
    residential_properties = ResidentialProperty.objects.filter(is_published=True).order_by('-listing_date')[:6]
    commercial_properties = CommercialProperty.objects.filter(is_published=True).order_by('-listing_date')[:6]
    industrial_properties = IndustrialProperty.objects.filter(is_published=True).order_by('-listing_date')[:6]

    # Fetch 6 objects for the general list
    all_properties = Property.objects.filter(is_published=True).order_by('-listing_date')[:6]

    context = {
        'land_properties': land_properties,
        'residential_properties': residential_properties,
        'commercial_properties': commercial_properties,
        'industrial_properties': industrial_properties,
        'all_properties': all_properties,
    }

    return render(request, 'property/property_index.html', context)


from django.shortcuts import get_object_or_404
from .models import Property, PropertyActions, PropertyUserTrack

def get_property_activity(property_id):
    """
    Fetch property activity details including likes, shares, views, comments, reports, and favourites.
    """
    activity_data = {
        "likes": 0,
        "shares": 0,
        "views": 0,
        "comments": 0,
        "reports": 0,
        "favourites": 0
    }

    # Fetch property actions (likes, shares, views, comments, reports for both auth users & guests)
    try:
        property_actions = PropertyActions.objects.get(property_id=property_id)
        counts = property_actions.activity_counts

        activity_data["likes"] = counts.get("auth_likes", 0) + counts.get("guest_likes", 0)
        activity_data["shares"] = counts.get("auth_shares", 0) + counts.get("guest_shares", 0)
        activity_data["views"] = counts.get("auth_views", 0) + counts.get("guest_views", 0)
        activity_data["comments"] = counts.get("auth_comments", 0)
        activity_data["reports"] = counts.get("auth_reports", 0)
    except PropertyActions.DoesNotExist:
        pass  # No actions recorded yet

    # Fetch all user records and count manually
    favourites_count = sum(
        1 for user_track in PropertyUserTrack.objects.all()
        if property_id in user_track.property_favourite
    )
    activity_data["favourites"] = favourites_count

    return activity_data
