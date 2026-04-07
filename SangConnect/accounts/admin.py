from django.contrib import admin
from .models import Donneur, Hopital

@admin.register(Hopital)
class HopitalAdmin(admin.ModelAdmin):
    list_display = ['nom', 'ville', 'agrement', 'valide']
    list_editable = ['valide']  # valider en un clic depuis la liste
    list_filter = ['valide', 'ville']

@admin.register(Donneur)
class DonneurAdmin(admin.ModelAdmin):
    list_display = ['user', 'groupe_sanguin', 'ville', 'actif', 'est_eligible']
    list_filter = ['groupe_sanguin', 'sexe', 'actif']