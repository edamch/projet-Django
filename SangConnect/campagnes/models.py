from django.db import models
from accounts.models import Hopital, Donneur

class Campagne(models.Model):
    hopital = models.ForeignKey(Hopital, on_delete=models.CASCADE)
    nom = models.CharField(max_length=200)
    date = models.DateField()
    lieu = models.CharField(max_length=200)
    groupes_cibles = models.CharField(max_length=50)
    capacite_totale = models.PositiveIntegerField()
    description = models.TextField(blank=True)

    def places_restantes(self):
        return self.capacite_totale - self.inscription_set.count()

    def __str__(self):
        return self.nom + " - " + self.hopital.nom + " - " + str(self.date) + " - " + self.lieu


class Inscription(models.Model):
    campagne = models.ForeignKey(Campagne, on_delete=models.CASCADE)
    donneur = models.ForeignKey(Donneur, on_delete=models.CASCADE)
    creneau_horaire = models.TimeField()
    date_inscription = models.DateTimeField(auto_now_add=True)
    present = models.BooleanField(default=False)
    