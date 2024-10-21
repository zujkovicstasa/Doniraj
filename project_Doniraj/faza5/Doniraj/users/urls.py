#Autor: Matija Milic 2021/0088
from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('registracija/',views.registracija, name = "registracija"),
    path('logovanje/',views.logovanje, name = "logovanje"),
    path('logout/',views.logout_view, name = "logout"),
    path('nalozi/',views.nalozi, name = "nalozi"),
    path('zahtevi/',views.zahtevi, name = "zahtevi"),
    path('zahtev/<int:id>/', views.zahtev, name='zahtev'),
    path('zahtev/<int:id>/approve/', views.approve_zahtev, name='approve_zahtev'),
    path('zahtev/<int:id>/reject/', views.reject_zahtev, name='reject_zahtev'),
    path('promenaLozinke/', views.promenaLozinke, name='promenaLozinke'),
    path('promenaSlike/', views.promenaSlike, name='promenaSlike'),
    path('delete_account/<int:user_id>/', views.delete_account, name='delete_account'),
    
    path('milica/<int:id>', views.milica, name = "milica"),

    path('zaboravljenaLozinka/', views.zaboravljenaLozinka, name = "zaboravljenaLozinka"),
    path('code_verify/', views.codeVerify, name='code_verify'),
    path('password_reset/', views.passwordReset, name='password_reset'),
]

