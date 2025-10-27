from django.contrib import admin
from .models import NotificationPreference, CategorySubscription, Notification


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_enabled', 'sms_enabled', 'push_enabled', 'in_app_enabled']
    list_filter = ['email_enabled', 'sms_enabled', 'push_enabled', 'in_app_enabled']
    search_fields = ['user__username', 'user__email']


@admin.register(CategorySubscription)
class CategorySubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'subscribed_at']
    list_filter = ['category', 'subscribed_at']
    search_fields = ['user__username', 'category__name']
    date_hierarchy = 'subscribed_at'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'title', 'is_read', 'sent_via', 'created_at']
    list_filter = ['notification_type', 'is_read', 'sent_via', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    readonly_fields = ['created_at', 'read_at']
    date_hierarchy = 'created_at'
    
    actions = ['mark_as_read']
    
    def mark_as_read(self, request, queryset):
        """Bulk action to mark notifications as read"""
        from django.utils import timezone
        updated = queryset.filter(is_read=False).update(
            is_read=True,
            read_at=timezone.now()
        )
        self.message_user(request, f'{updated} notifications marked as read.')
    mark_as_read.short_description = "Mark selected notifications as read"
