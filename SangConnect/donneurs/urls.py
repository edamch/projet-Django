from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.donneur_dashboard, name='donneur_dashboard'),
    path('repondre/<int:demande_id>/', views.repondre_appel, name='repondre_appel'),
    path('don/enregistrer/', views.enregistrer_don, name='enregistrer_don'),
]