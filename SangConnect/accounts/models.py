from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta

GROUPES_SANGUINS = [
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
    ('O+', 'O+'), ('O-', 'O-'),
]

class Donneur(models.Model):
    SEXE_CHOICES = [('M', 'Masculin'), ('F', 'Féminin')]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    groupe_sanguin = models.CharField(max_length=3, choices=GROUPES_SANGUINS)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    date_naissance = models.DateField()
    ville = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, blank=True)
    actif = models.BooleanField(default=True)

    def prochaine_date_don(self):
        dernier_don = self.don_set.order_by('-date_don').first()
        if not dernier_don:
            return date.today() 
        delai = 56 if self.sexe == 'M' else 84
        return dernier_don.date_don + timedelta(days=delai)

    def est_eligible(self):
        return date.today() >= self.prochaine_date_don() and self.actif

    def __str__(self):
        return self.groupe_sanguin + " - " + self.sexe + " - " + str(self.date_naissance) + " - " + self.ville + " - " + self.telephone


class Hopital(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=200)
    adresse = models.TextField()
    ville = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    agrement = models.CharField(max_length=50, unique=True)
    valide = models.BooleanField(default=False) 

    def __str__(self):
        return self.nom + " - " + self.adresse + " - " + self.ville + " - " + self.telephone + " - " + self.agrement