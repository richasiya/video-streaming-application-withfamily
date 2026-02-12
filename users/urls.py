from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('watchlist/', views.watchlist_view, name='watchlist'),
    path('watchlist/toggle/<slug:slug>/', views.watchlist_toggle_view, name='watchlist_toggle'),
    path('history/', views.history_view, name='history'),
    path('history/clear/', views.clear_history_view, name='clear_history'),
    path('plan/', views.choose_plan_view, name='choose_plan'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('payment/verify/', views.payment_verify_view, name='payment_verify'),
    path('logout/', views.logout_view, name='logout'),
]

