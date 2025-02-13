from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


def redirecione(request):
    return redirect('auth/login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('usuarios.urls')),
    path("divulgar/", include('divulgar.urls')),
    path('adotar/', include('adotar.urls')),
    path('', redirecione)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
