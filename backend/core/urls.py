from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect


def redirect_to_login(request):
    """redireciona o root para login"""
    return redirect('login/')


urlpatterns = [
    path('__reload__/', include("django_browser_reload.urls")),
    path('', redirect_to_login),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include('control.urls')),
]

# Configuração para as imagens
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)