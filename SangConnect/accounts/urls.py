from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('inscription/donneur/', views.inscription_donneur, name='inscription_donneur'),
    path('inscription/hopital/', views.inscription_hopital, name='inscription_hopital'),
    path('login/', views.connexion, name='login'),
    path('logout/', views.deconnexion, name='logout'),
]