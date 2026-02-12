from django.contrib.auth.models import User
from django.db import models
from content.models import Content

class UserProfile(models.Model):

    SUBSCRIPTION_CHOICES = [
        ('free', 'Free'),
        ('basic', 'Basic'),
        ('premium', 'Premium'),
    ]
    STATUS_CHOICES = [
        ('free', 'Free'),
        ('active', 'Active'),
        ('canceled', 'Canceled'),
        ('past_due', 'Past Due'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    # 🔥 NEW FIELDS
    mobile = models.CharField(max_length=15, blank=True)
    dob = models.DateField(null=True, blank=True)
    subscription = models.CharField(
        max_length=20,
        choices=SUBSCRIPTION_CHOICES,
        default='free'
    )
    subscription_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='free'
    )
    plan_confirmed = models.BooleanField(default=False)
    last_payment_id = models.CharField(max_length=120, blank=True)
    last_order_id = models.CharField(max_length=120, blank=True)
    subscription_updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class PaymentTransaction(models.Model):
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=20, choices=UserProfile.SUBSCRIPTION_CHOICES)
    amount = models.PositiveIntegerField()  # amount in paise
    currency = models.CharField(max_length=10, default='INR')
    razorpay_order_id = models.CharField(max_length=120, blank=True)
    razorpay_payment_id = models.CharField(max_length=120, blank=True)
    razorpay_signature = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan} - {self.status}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content')

    def __str__(self):
        return f"{self.user.username} - {self.content.title}"


class WatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    last_watched_at = models.DateTimeField(auto_now=True)
    watch_count = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'content')

    def __str__(self):
        return f"{self.user.username} - {self.content.title}"
