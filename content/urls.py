from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('movies/', views.movies_view, name='movies'),
    path('webseries/', views.webseries_view, name='webseries'),
    path('shortfilm/', views.shortfilm_view, name='shortfilm'),
    path('podcasts/', views.podcast_view, name='podcasts'),
    path('watch/<slug:slug>/', views.watch_view, name='content_watch'),
    
]