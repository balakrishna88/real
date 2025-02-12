from django.contrib import admin
from .models import Room, Message, Group, GroupStats, GroupMessage, GroupJoinRequest, GroupReport, MessageReaction, MessageEditHistory, Notification, AutoDeleteMessages
from account.models import Account

# ------------------ ROOM CHAT MODELS ------------------

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_participants')
    search_fields = ('name',)
    
    def get_participants(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])
    get_participants.short_description = 'Participants'

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'room', 'content', 'timestamp', 'is_deleted')
    search_fields = ('room__name', 'sender__username', 'content')
    list_filter = ('room', 'is_deleted')

# ------------------ GROUP CHAT MODELS ------------------

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'group_type', 'created_at', 'get_participants', 'get_admins', 'get_moderators')
    search_fields = ('name',)
    list_filter = ('group_type',)
    
    def get_participants(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])
    get_participants.short_description = 'Participants'
    
    def get_admins(self, obj):
        return ", ".join([user.username for user in obj.admins.all()])
    get_admins.short_description = 'Admins'
    
    def get_moderators(self, obj):
        return ", ".join([user.username for user in obj.moderators.all()])
    get_moderators.short_description = 'Moderators'

class GroupStatsAdmin(admin.ModelAdmin):
    list_display = ('group', 'total_messages', 'total_participants', 'total_views', 'total_likes', 'total_shares', 'total_reports')
    search_fields = ('group__name',)

# ------------------ GROUP MESSAGE MODEL ------------------

class GroupMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'group', 'content', 'timestamp', 'is_deleted')
    search_fields = ('group__name', 'sender__username', 'content')
    list_filter = ('group', 'is_deleted')

# ------------------ GROUP JOIN REQUESTS ------------------

class GroupJoinRequestAdmin(admin.ModelAdmin):
    list_display = ('group', 'user', 'status', 'timestamp')
    search_fields = ('group__name', 'user__username')
    list_filter = ('status',)

# ------------------ GROUP REPORTS ------------------

class GroupReportAdmin(admin.ModelAdmin):
    list_display = ('group', 'reported_by', 'reason', 'timestamp')
    search_fields = ('group__name', 'reported_by__username', 'reason')

# ------------------ MESSAGE REACTIONS ------------------

class MessageReactionAdmin(admin.ModelAdmin):
    list_display = ('message', 'user', 'emoji')
    search_fields = ('message__content', 'user__username', 'emoji')
    list_filter = ('emoji',)

# ------------------ MESSAGE EDIT HISTORY ------------------

class MessageEditHistoryAdmin(admin.ModelAdmin):
    list_display = ('message', 'old_content', 'edited_at')
    search_fields = ('message__content', 'old_content')

# ------------------ NOTIFICATIONS ------------------

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'notification_type', 'is_read', 'timestamp')
    search_fields = ('user__username', 'message', 'notification_type')
    list_filter = ('notification_type', 'is_read')

# ------------------ AUTO-DELETE SETTINGS ------------------

class AutoDeleteMessagesAdmin(admin.ModelAdmin):
    list_display = ('group', 'delete_after_days')
    search_fields = ('group__name',)

# ------------------ Register Models ------------------

admin.site.register(Room, RoomAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(GroupStats, GroupStatsAdmin)
admin.site.register(GroupMessage, GroupMessageAdmin)
admin.site.register(GroupJoinRequest, GroupJoinRequestAdmin)
admin.site.register(GroupReport, GroupReportAdmin)
admin.site.register(MessageReaction, MessageReactionAdmin)
admin.site.register(MessageEditHistory, MessageEditHistoryAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(AutoDeleteMessages, AutoDeleteMessagesAdmin)
