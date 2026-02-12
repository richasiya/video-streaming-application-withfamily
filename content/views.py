from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Content
from users.models import WatchHistory
from django.utils import timezone
from django.shortcuts import get_object_or_404

def home_view(request):
    featured = Content.objects.order_by('-created_at')[:6]
    recent_history = []
    if request.user.is_authenticated:
        recent_history = WatchHistory.objects.filter(user=request.user).select_related('content').order_by('-last_watched_at')[:6]
    return render(request, 'content/home.html', {
        'featured': featured,
        'recent_history': recent_history
    })

def movies_view(request):
    movies = Content.objects.filter(content_type='movie')
    return render(request, 'content/movies.html', {'movies': movies})

def webseries_view(request):
    webseries = Content.objects.filter(content_type='webseries')
    return render(request, 'content/webseries.html', {'webseries': webseries})

def shortfilm_view(request):
    shortfilms = Content.objects.filter(content_type='shortfilm')
    return render(request, 'content/shortfilm.html', {'shortfilms': shortfilms})

def podcast_view(request):
    podcasts = Content.objects.filter(content_type='podcast')
    return render(request, 'content/podcast.html', {'podcasts': podcasts})


PLAN_RANK = {
    'free': 0,
    'basic': 1,
    'premium': 2,
}


def user_can_access(user, item):
    if not user.is_authenticated:
        return False
    profile = getattr(user, 'userprofile', None)
    if not profile:
        return False
    return PLAN_RANK.get(profile.subscription, 0) >= PLAN_RANK.get(item.access_level, 0)



@login_required
def watch_view(request, slug):
    item = get_object_or_404(Content, slug=slug)
    if not user_can_access(request.user, item):
        return render(request, 'content/upgrade.html', {
            'item': item,
            'required_plan': item.access_level
        })
    history, created = WatchHistory.objects.get_or_create(user=request.user, content=item)
    if not created:
        history.watch_count += 1
    history.last_watched_at = timezone.now()
    history.save()
    # use Content.video_src property which looks in MEDIA, external URL, then project video/
    video_src = item.video_src
    related = Content.objects.filter(content_type=item.content_type).exclude(id=item.id).order_by('-created_at')[:6]
    return render(request, 'content/watch.html', {
        'item': item,
        'video_src': video_src,
        'related': related
    })
