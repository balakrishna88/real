from django.db import models
from account.models import Account
from django.utils.timezone import now
from datetime import timedelta

# ------------------ ROOM CHAT MODELS ------------------

from django.utils.text import slugify

class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)  # Add the slug field
    participants = models.ManyToManyField(Account, related_name='chat_rooms')

    def save(self, *args, **kwargs):
        # Automatically generate the slug based on the name field if slug is empty
        if not self.slug:
            self.slug = slugify(self.name)

        # Ensure the slug is unique by checking for existing slugs
        original_slug = self.slug
        counter = 1
        while Room.objects.filter(slug=self.slug).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(Account, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def delete_message(self):
        self.content = "[Message deleted]"
        self.is_deleted = True
        self.save()

    def __str__(self):
        return f'{self.sender} in {self.room}: {self.content[:30]}'


# ------------------ GROUP CHAT MODELS ------------------

# models.py


from django.utils.text import slugify
from django.db import models

from django.utils.text import slugify
from django.db import models

class Group(models.Model):
    PUBLIC = 'public'
    PRIVATE = 'private'
    OFFICIAL = 'official'
    GROUP_TYPES = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
        (OFFICIAL, 'Official'),
    ]

    PUBLISHED = 'published'
    FROZEN = 'frozen'
    DRAFT = 'draft'
    GROUP_STATUS = [
        (PUBLISHED, 'Published'),
        (FROZEN, 'Frozen'),
        (DRAFT, 'Draft'),
    ]

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    group_type = models.CharField(max_length=10, choices=GROUP_TYPES, default=PUBLIC)
    participants = models.ManyToManyField(Account, related_name='groups', blank=True)
    admins = models.ManyToManyField(Account, related_name='group_admins')
    moderators = models.ManyToManyField(Account, related_name='group_moderators', blank=True)
    banned_users = models.ManyToManyField(Account, related_name='banned_from_groups', blank=True)
    logo = models.ImageField(upload_to='group_logos/', blank=True, null=True)
    requires_approval = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Add a status field for group management
    status = models.CharField(max_length=10, choices=GROUP_STATUS, default=PUBLISHED)

    def save(self, *args, **kwargs):
        # Automatically generate the slug based on the name field
        if not self.slug:
            self.slug = slugify(self.name)

        # Ensure the slug is unique by checking for existing slugs
        original_slug = self.slug
        counter = 1
        while Group.objects.filter(slug=self.slug).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name





# ------------------ GROUP STATISTICS ------------------

class GroupStats(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='stats')
    total_messages = models.PositiveIntegerField(default=0)
    total_participants = models.PositiveIntegerField(default=0)
    total_views = models.PositiveIntegerField(default=0)
    total_likes = models.PositiveIntegerField(default=0)
    total_shares = models.PositiveIntegerField(default=0)
    total_reports = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Stats for {self.group.name}'


# ------------------ GROUP MESSAGE MODEL ------------------

class GroupMessage(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(Account, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='group_chat_files/', blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def delete_message(self):
        self.content = "[Message deleted]"
        self.is_deleted = True
        self.save()

    def __str__(self):
        return f'{self.sender} in {self.group}: {self.content[:30]}'


# ------------------ GROUP JOIN REQUESTS ------------------

class GroupJoinRequest(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='join_requests')
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending'
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Join Request: {self.user} -> {self.group}'


# ------------------ GROUP REPORTS ------------------

class GroupReport(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='reports')
    reported_by = models.ForeignKey(Account, on_delete=models.CASCADE)
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Report: {self.reported_by} -> {self.group}'


# ------------------ MESSAGE REACTIONS ------------------

class MessageReaction(models.Model):
    message = models.ForeignKey(GroupMessage, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    emoji = models.CharField(max_length=10)

    class Meta:
        unique_together = ('message', 'user')

    def __str__(self):
        return f'{self.user} reacted {self.emoji} to {self.message}'


# ------------------ MESSAGE EDIT HISTORY ------------------

class MessageEditHistory(models.Model):
    message = models.ForeignKey(GroupMessage, on_delete=models.CASCADE, related_name='edit_history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Edit history for message {self.message.id}'


# ------------------ NOTIFICATIONS ------------------

class Notification(models.Model):
    JOIN_REQUEST = 'join_request'
    GROUP_REPORT = 'group_report'
    CHAT_REQUEST = 'chat_request'
    MOBILE_REQUEST = 'mobile_request'

    NOTIFICATION_TYPES = [
        (JOIN_REQUEST, 'Join Request'),
        (GROUP_REPORT, 'Group Report'),
        (CHAT_REQUEST, 'Chat Request'),
        (MOBILE_REQUEST, 'Mobile Request'),
    ]

    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.user.username} - {self.notification_type}'



# ------------------ AUTO-DELETE SETTINGS ------------------

class AutoDeleteMessages(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='auto_delete_settings')
    delete_after_days = models.PositiveIntegerField(default=90)

    def delete_old_messages(self):
        threshold_date = now() - timedelta(days=self.delete_after_days)
        GroupMessage.objects.filter(group=self.group, timestamp__lt=threshold_date).delete()

    def __str__(self):
        return f'Auto-delete messages older than {self.delete_after_days} days in {self.group}'



# ------------------ PUSH NOTIFICATIONS ------------------

class PushNotification(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='push_notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Push Notification for {self.user.username} - {self.title}'
