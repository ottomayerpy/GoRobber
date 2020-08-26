from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('support/', include('support.urls')),
    path('case/', include('case.urls')),
    path('admin/', admin.site.urls),
    path('profile/', include('profile.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('home.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
