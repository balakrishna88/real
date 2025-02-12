from django.shortcuts import get_object_or_404, render

from account.models import Account
from .models import GroupMessage, Room
from django.shortcuts import render, redirect
from .models import Room
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from .models import Room

# View for the room list page (no authentication required)
def room_list(request):
    # Fetch all rooms (no filtering based on participants)
    rooms = Room.objects.all()

    # Render the template with the fetched rooms
    return render(request, 'chat/room/room_list.html', {'rooms': rooms})



# View for the room detail page
def room_detail(request, id):  # Ensure 'id' is part of the function signature
    # Fetch the room by its ID (or return a 404 if not found)
    room = get_object_or_404(Room, id=id)
    
    # Fetch messages related to this room (optional, if you want to display messages)
    messages = room.messages.all()
    
    # Render the room detail template
    return render(request, 'chat/room/room_detail.html', {'room': room, 'messages': messages})


from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .models import Room, Notification

def create_room(request):
    User = get_user_model()
    users = User.objects.exclude(id=request.user.id)  # Exclude the current user

    if request.method == 'POST':
        selected_user_id = request.POST.get('selected_user')  
        selected_user = User.objects.get(id=selected_user_id)

        # Create a new chat room
        room = Room.objects.create(name=f"Room with {selected_user.username}")
        room.participants.add(request.user, selected_user)

        # Create a notification for the selected user
        Notification.objects.create(
            user=selected_user,
            message=f"{request.user.username} created a new chat room with you.",
            notification_type=Notification.CHAT_REQUEST
        )

        # Redirect to the room list
        return redirect('room_list')

    return render(request, 'chat/room/create_room.html', {'users': users})



# View for deleting a room
def delete_room(request, room_id):
    return render(request, 'chat/room/delete_room.html')

# View for adding participants to a room
def add_participants(request, room_id):
    return render(request, 'chat/room/add_participants.html')





from django.shortcuts import render
from .models import Message

# View for message history
def message_history(request, room_id):
    return render(request, 'chat/message/message_history.html')

# View for sending a message
def send_message(request, room_id):
    return render(request, 'chat/message/send_message.html')

# View for deleting a message
def delete_message(request, message_id):
    return render(request, 'chat/message/delete_message.html')

# View for editing a message
def edit_message(request, message_id):
    return render(request, 'chat/message/edit_message.html')

# View for reacting to a message
def react_to_message(request, message_id):
    return render(request, 'chat/message/react_to_message.html')



from django.shortcuts import render
from .models import Group

# View for the group list page

from django.shortcuts import render
from .models import Group, GroupJoinRequest

def group_list(request):
    # Fetch all groups
    groups = Group.objects.all()

    # Filter groups into public and private
    public_groups = groups.filter(group_type='public')
    private_groups = groups.filter(group_type='private')

    # Prepare data for private groups
    if request.user.is_authenticated:
        private_groups_data = []
        for group in private_groups:
            is_participant = request.user in group.participants.all()
            has_pending_request = GroupJoinRequest.objects.filter(
                group=group,
                user=request.user,
                status='pending'
            ).exists()

            private_groups_data.append({
                'group': group,
                'is_participant': is_participant,
                'has_pending_request': has_pending_request,
            })
    else:
        private_groups_data = [{'group': group} for group in private_groups]

    return render(request, 'chat/group/group_list.html', {
        'public_groups': public_groups,
        'private_groups_data': private_groups_data,
        'user_authenticated': request.user.is_authenticated,
    })




from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Group, GroupMessage, GroupStats

@login_required  # Ensure only authenticated users can access this view
def group_detail(request, group_name):
    # Fetch the group by ID or return a 404 error if not found
    group = get_object_or_404(Group, name=group_name)

    # Check if the user is banned from the group
    if request.user in group.banned_users.all():
        return render(request, 'chat/group/access_denied.html', status=403)  # Render a "banned" page
    
    # If the group is private or official, check if the user is a participant
    if group.group_type in [Group.PRIVATE, Group.OFFICIAL]:
        if request.user not in group.participants.all():
            # Redirect or show an error message if the user is not a participant
            return render(request, 'chat/group/access_denied.html', status=403)

    # If the group is public, automatically add the user as a participant
    if group.group_type == Group.PUBLIC:
        if request.user not in group.participants.all():
            group.participants.add(request.user)  # Add the user as a participant

    # Fetch group messages, ordered by timestamp
    messages = GroupMessage.objects.filter(group=group).order_by('-timestamp')

    # Fetch stats for the group from GroupStats (or create a new one if not exists)
    group_stats, created = GroupStats.objects.get_or_create(group=group)

    # Calculate the total views, likes, shares, reports
    total_views = group_stats.total_views
    total_likes = group_stats.total_likes
    total_shares = group_stats.total_shares
    total_reports = group_stats.total_reports

    # Count the total participants
    total_participants = group.participants.count()

    # Count the total messages in the group
    total_messages = messages.count()

    # Check if the user has already viewed the group in this session
    session_key = f"viewed_group_{group_name}"
    if not request.session.get(session_key, False):
        group_stats.total_views += 1  # Increment view count
        group_stats.save()
        request.session[session_key] = True  # Mark as viewed in session

    return render(request, 'chat/group/group_detail.html', {
        'group': group,
        'messages': messages,
        'total_messages': total_messages,
        'total_participants': total_participants,
        'total_views': total_views,
        'total_likes': total_likes,
        'total_shares': total_shares,
        'total_reports': total_reports,
    })






from django.shortcuts import render, redirect
from django.contrib import messages  # For displaying error messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Group
import re

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Group, Notification

@login_required
def create_group(request):
    if request.method == 'POST':
        # Get form data from the POST request
        name = request.POST.get('name')
        description = request.POST.get('description')
        group_type = request.POST.get('group_type')

        # Check if the group name contains spaces
        if ' ' in name:
            messages.error(request, "Group name cannot contain spaces. Please choose a different name.")
            return render(request, 'chat/group/create_group.html')

        # Check if the group name is unique
        if Group.objects.filter(name=name).exists():
            messages.error(request, "A group with this name already exists. Please choose another name.")
            return render(request, 'chat/group/create_group.html')

        # Create a new group if the name is unique and valid
        group = Group.objects.create(
            name=name,
            description=description,
            group_type=group_type,
            created_at=timezone.now()
        )

        # Assign the creator as an admin and participant
        group.admins.add(request.user)
        group.participants.add(request.user)

        # Create a notification for the group creator
        Notification.objects.create(
            user=request.user,
            message=f"You created a new group: {group.name}.",
            notification_type=Notification.JOIN_REQUEST
        )

        # Redirect to the group detail page
        return redirect('group_detail', group_name=group.name)

    # Render the create group form
    return render(request, 'chat/group/create_group.html')





from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Group


@login_required
def group_join(request, group_name):
    group = get_object_or_404(Group, name__iexact=group_name)  # Case-insensitive lookup
    group_stats, created = GroupStats.objects.get_or_create(group=group)

    if request.user not in group.participants.all():
        group.participants.add(request.user)
        group_stats.total_participants = group.participants.count()
        group_stats.save()  # Update stats when user joins
        messages.success(request, f"You have successfully joined {group.name}!")

    return redirect('group_detail', group_name=group.name)





    

# views.py
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from .models import GroupStats, Group

def update_group_stats(request, group_id, stat_type):
    group = get_object_or_404(Group, id=group_id)
    group_stats, created = GroupStats.objects.get_or_create(group=group)

    if request.method == 'POST':
        if stat_type == 'message':
            group_stats.total_messages += 1
        elif stat_type == 'participant':
            # Update total participants dynamically
            group_stats.total_participants = group.participants.count()
        elif stat_type == 'view':
            group_stats.total_views += 1
        elif stat_type == 'like':
            group_stats.total_likes += 1
        elif stat_type == 'share':
            group_stats.total_shares += 1
        elif stat_type == 'report':
            group_stats.total_reports += 1

        group_stats.save()  # Save the updated stats

        return redirect('group_detail', group_name=group.name)

    return HttpResponse("Invalid request method.")



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from .models import Group, GroupReport, GroupStats

@login_required
def report_group(request, group_id):
    if request.method == "POST":
        group = get_object_or_404(Group, id=group_id)
        reason = request.POST.get("reason", "").strip()  # Get the reason from the form

        if not reason:
            return HttpResponseBadRequest("Reason is required.")

        # 1️⃣ Create and save the report
        GroupReport.objects.create(group=group, reported_by=request.user, reason=reason)

        # 2️⃣ Update the group stats (same as `update_group_stats` function)
        group_stats, created = GroupStats.objects.get_or_create(group=group)
        group_stats.total_reports += 1
        group_stats.save()

        return redirect("group_detail", group_name=group.name)  # Redirect after reporting
    
    return HttpResponseBadRequest("Invalid request method.")


# View for group settings page
# views.py
from django.shortcuts import render
from .models import Group

def group_settings(request):
    # Fetch the authenticated user
    user = request.user

    # Fetch groups where the user is an admin
    admin_groups = Group.objects.filter(admins=user)

    # Fetch groups where the user is a participant (but not an admin)
    participant_groups = Group.objects.filter(participants=user).exclude(admins=user)

    return render(request, 'chat/group/group_settings.html', {
        'admin_groups': admin_groups,
        'participant_groups': participant_groups,
    })



# views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from .models import Group

@login_required
def manage_group(request, group_id):
    # Fetch the group by ID or return a 404 error if not found
    group = get_object_or_404(Group, id=group_id)


    # Ensure the user is an admin of the group
    if request.user not in group.admins.all():
        raise PermissionDenied("You do not have permission to manage this group.")
    
    # Fetch all join requests for this group
    join_requests = GroupJoinRequest.objects.filter(group=group, status='pending')
    
    
    # Handle adding a participant
    if request.method == 'POST' and 'add_participant' in request.POST:
        username = request.POST.get('username')
        try:
            user_to_add = Account.objects.get(username=username)
            if user_to_add not in group.participants.all() and user_to_add not in group.banned_users.all():
                group.participants.add(user_to_add)
                messages.success(request, f"{user_to_add.username} has been added as a participant.")
            elif user_to_add in group.banned_users.all():
                messages.error(request, f"{user_to_add.username} is banned and cannot be added as a participant.")
            else:
                messages.warning(request, f"{user_to_add.username} is already a participant.")
        except Account.DoesNotExist:
            messages.error(request, "User does not exist.")

    # Handle removing a participant
    if request.method == 'POST' and 'remove_participant' in request.POST:
        user_id = request.POST.get('user_id')
        try:
            user_to_remove = Account.objects.get(id=user_id)
            if user_to_remove in group.participants.all():
                group.participants.remove(user_to_remove)
                messages.success(request, f"{user_to_remove.username} has been removed from the group.")
            else:
                messages.warning(request, f"{user_to_remove.username} is not a participant.")
        except Account.DoesNotExist:
            messages.error(request, "User does not exist.")

    # Handle banning a user
    if request.method == 'POST' and 'ban_user' in request.POST:
        user_id = request.POST.get('user_id')
        try:
            user_to_ban = Account.objects.get(id=user_id)
            if user_to_ban not in group.banned_users.all():
                group.banned_users.add(user_to_ban)
                group.participants.remove(user_to_ban)  # Remove the user from participants
                messages.success(request, f"{user_to_ban.username} has been banned from the group.")
            else:
                messages.warning(request, f"{user_to_ban.username} is already banned.")
        except Account.DoesNotExist:
            messages.error(request, "User does not exist.")

    # Handle unbanning a user
    if request.method == 'POST' and 'unban_user' in request.POST:
        user_id = request.POST.get('user_id')
        try:
            user_to_unban = Account.objects.get(id=user_id)
            if user_to_unban in group.banned_users.all():
                group.banned_users.remove(user_to_unban)  # Remove the user from banned_users
                if user_to_unban not in group.participants.all():
                    group.participants.add(user_to_unban)  # Add the user back to participants
                messages.success(request, f"{user_to_unban.username} has been unbanned and restored as a participant.")
            else:
                messages.warning(request, f"{user_to_unban.username} is not banned.")
        except Account.DoesNotExist:
            messages.error(request, "User does not exist.")
    


    # Handle updating group details
    if request.method == 'POST' and 'update_group' in request.POST:
        # Update name
        name = request.POST.get('name')
        if name != group.name:
            group.name = name
            messages.success(request, "Group name has been updated.")

        # Update description
        description = request.POST.get('description')
        if description != group.description:
            group.description = description
            messages.success(request, "Group description has been updated.")

        # Update status
        status = request.POST.get('status')
        if status != group.status:
            group.status = status
            messages.success(request, "Group status has been updated.")

        # Update logo
        logo_file = request.FILES.get('logo')
        if logo_file:
            group.logo = logo_file
            messages.success(request, "The group logo has been updated.")

        # Save changes to the group
        group.save()

        # Redirect back to the same page after saving
        return redirect('manage_group', group_id=group.id)

    # Separate admins and participants (excluding admins)
    admins = group.admins.all()
    participants_excluding_admins = group.participants.exclude(id__in=admins.values_list('id', flat=True))

  

    # Pass the group details, admins, and participants to the template
    return render(request, 'chat/group/group_manage.html', {
        'group': group,
        'admins': admins,
        'participants_excluding_admins': participants_excluding_admins,
        'join_requests': join_requests
        
        
    })


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseBadRequest
from .models import Group, GroupJoinRequest

def request_to_join_group(request, group_id):
    # Ensure the request method is POST
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method.")

    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to request to join a group.")
        return redirect('group_list')  # Redirect to the group list page or login page

    # Get the group object
    group = get_object_or_404(Group, id=group_id)

    # Check if the user has already submitted a pending request
    if GroupJoinRequest.objects.filter(group=group, user=request.user, status='pending').exists():
        messages.warning(request, "You have already requested to join this group.")
        return redirect(request.META.get('HTTP_REFERER', 'group_list'))  # Redirect back to the same page

    # Create a new join request
    GroupJoinRequest.objects.create(
        group=group,
        user=request.user,
        status='pending'
    )
    messages.success(request, f"Your request to join '{group.name}' has been submitted.")

    # Redirect back to the same page
    return redirect(request.META.get('HTTP_REFERER', 'group_list'))


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import GroupJoinRequest, GroupStats

def approve_join_request(request, request_id):
    # Fetch the join request
    join_request = get_object_or_404(GroupJoinRequest, id=request_id)

    # Update the status to "approved"
    join_request.status = 'approved'
    join_request.save()

    # Add the user to the group's participants
    join_request.group.participants.add(join_request.user)

    # Update group stats
    group_stats, created = GroupStats.objects.get_or_create(group=join_request.group)
    group_stats.total_participants = join_request.group.participants.count()
    group_stats.save()

    messages.success(request, f"Join request from {join_request.user.username} has been approved.")
    return redirect('manage_group', group_id=join_request.group.id)



from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import GroupJoinRequest

def reject_join_request(request, request_id):
    # Fetch the join request
    join_request = get_object_or_404(GroupJoinRequest, id=request_id)

    # Update the status to "rejected"
    join_request.status = 'rejected'
    join_request.save()

    messages.success(request, f"Join request from {join_request.user.username} has been rejected.")
    return redirect('manage_group', group_id=join_request.group.id)


from django.shortcuts import render
from .models import Notification

# View for the user's notification list
def notification_list(request):
    return render(request, 'chat/notification/notification_list.html')

# View for the notification details
def notification_detail(request, notification_id):
    return render(request, 'chat/notification/notification_detail.html')




from django.shortcuts import render
from .models import PushNotification

# View for the user's push notification list
def push_notification_list(request):
    return render(request, 'push_notification/push_notification_list.html')

# View for sending a push notification
def send_push_notification(request):
    return render(request, 'push_notification/send_push_notification.html')

