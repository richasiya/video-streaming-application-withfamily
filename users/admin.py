from django.contrib import admin
from .models import UserProfile, PaymentTransaction, Watchlist, WatchHistory


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'subscription', 'subscription_status', 'plan_confirmed')
	search_fields = ('user__username',)


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
	list_display = ('user', 'plan', 'amount', 'currency', 'status', 'created_at')
	list_filter = ('status', 'plan', 'currency')
	search_fields = ('user__username', 'razorpay_order_id', 'razorpay_payment_id')


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
	list_display = ('user', 'content', 'created_at')
	list_filter = ('created_at',)
	search_fields = ('user__username', 'content__title')


@admin.register(WatchHistory)
class WatchHistoryAdmin(admin.ModelAdmin):
	list_display = ('user', 'content', 'watch_count', 'last_watched_at')
	list_filter = ('last_watched_at',)
	search_fields = ('user__username', 'content__title')
