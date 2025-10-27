from django.db import models
from django.contrib.auth.models import User
from events.models import Event, EventCategory


class NotificationPreference(models.Model):
    """User preferences for receiving notifications"""
    NOTIFICATION_METHODS = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
        ('in_app', 'In-App'),
    ]
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='notification_preference'
    )
    email_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=False)
    push_enabled = models.BooleanField(default=True)
    in_app_enabled = models.BooleanField(default=True)
    
    # Notification frequency
    immediate = models.BooleanField(
        default=True,
        help_text="Send notifications immediately when new events are posted"
    )
    daily_digest = models.BooleanField(
        default=False,
        help_text="Receive daily digest of events"
    )
    weekly_digest = models.BooleanField(
        default=False,
        help_text="Receive weekly digest of events"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Notification preferences for {self.user.username}"


class CategorySubscription(models.Model):
    """Track which event categories users are subscribed to"""
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='category_subscriptions'
    )
    category = models.ForeignKey(
        EventCategory, 
        on_delete=models.CASCADE, 
        related_name='subscribers'
    )
    subscribed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'category']
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return f"{self.user.username} subscribed to {self.category.name}"


class Notification(models.Model):
    """Model for storing notifications sent to users"""
    NOTIFICATION_TYPES = [
        ('new_event', 'New Event'),
        ('event_update', 'Event Updated'),
        ('event_reminder', 'Event Reminder'),
        ('event_cancelled', 'Event Cancelled'),
        ('registration_confirmation', 'Registration Confirmed'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    event = models.ForeignKey(
        Event, 
        on_delete=models.CASCADE, 
        related_name='notifications',
        null=True,
        blank=True
    )
    notification_type = models.CharField(
        max_length=30, 
        choices=NOTIFICATION_TYPES
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    sent_via = models.CharField(max_length=20, default='in_app')
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.notification_type} for {self.user.username}: {self.title}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        from django.utils import timezone
        self.is_read = True
        self.read_at = timezone.now()
        self.save()
