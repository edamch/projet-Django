from django.db import models
from accounts.models import Donneur, Hopital
from hopitaux.models import DemandeUrgente

class Don(models.Model):
    donneur = models.ForeignKey(Donneur, on_delete=models.CASCADE)
    hopital = models.ForeignKey(Hopital, on_delete=models.SET_NULL, null=True)
    date_don = models.DateField()
    notes = models.TextField(blank=True)
    valide = models.BooleanField(default=False)

    def __str__(self):
        return self.donneur.user.username + " - " + self.hopital.nom + " - " + str(self.date_don)


class ReponseAppel(models.Model):
    STATUT = [
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé'),
    ]
    donneur = models.ForeignKey(Donneur, on_delete=models.CASCADE)
    demande = models.ForeignKey(DemandeUrgente, on_delete=models.CASCADE)
    date_reponse = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT, default='en_attente')