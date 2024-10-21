from django.urls import path
from . import views
#Autor: Lazar Krpovic 2021/0633
app_name = 'oglasi'

urlpatterns = [
    path('', views.pocetna , name="home"),
    path('oglas/<int:oglas_id>/', views.oglas, name='oglas'),
    path('fetch_oglases/', views.fetch_oglases, name='fetch_oglases'),
    path('postaviOglas/', views.postaviOglas, name = "postaviOglas"),
    path('search/', views.search, name='search'),
    path('delete_oglas/<int:oglas_id>/', views.deleteOglas, name = "deleteOglas"),
]

