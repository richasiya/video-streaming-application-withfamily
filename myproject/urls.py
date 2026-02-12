from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('content.urls')),
    path('users/', include('users.urls')),
    path('favicon.ico', lambda request: HttpResponse(status=204)),
    path('.well-known/appspecific/com.chrome.devtools.json', lambda request: HttpResponse(status=204)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
