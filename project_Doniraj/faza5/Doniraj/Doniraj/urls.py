
from django.contrib import admin
from django.urls import include, path
from . import views
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

#Author:Marija Stakic 2021/0320

urlpatterns = [
    path('admin/', admin.site.urls),

    path('organizacije/', views.organizacije, name='organizacije'),
    path('organizacijaProfil/', views.organizacijaProfil),
    path('organizacijaOglas/<int:organization_id>/', views.organizacijaOglas, name='organizacijaOglas'),

    path('inbox/', views.inbox),
    path('chat/', include('chat.urls')),
   

    path('users/',include('users.urls')),

    path('', RedirectView.as_view(url='/oglasi/', permanent=True)),
    path('oglasi/', include('oglasi.urls')),  


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)