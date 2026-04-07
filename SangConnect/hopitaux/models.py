from django.db import models
from accounts.models import Hopital, GROUPES_SANGUINS

STATUT_DEMANDE = [
    ('active', 'Active'),
    ('satisfaite', 'Satisfaite'),
    ('cloturee', 'Clôturée'),
]

class DemandeUrgente(models.Model):
    hopital = models.ForeignKey(Hopital, on_delete=models.CASCADE)
    groupe_sanguin = models.CharField(max_length=3, choices=GROUPES_SANGUINS)
    quantite = models.PositiveIntegerField(help_text="Nombre de poches")
    delai = models.DateField(help_text="Date limite")
    description = models.TextField(blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_DEMANDE, default='active')
    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.hopital.nom + " - " + self.groupe_sanguin + " - " + str(self.quantite) + " poches - " + self.statut
    