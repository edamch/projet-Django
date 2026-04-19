from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.hopital_dashboard, name='hopital_dashboard'),
    path('demande/publier/', views.publier_demande, name='publier_demande'),
    path('demande/cloturer/<int:demande_id>/', views.cloturer_demande, name='cloturer_demande'),
]