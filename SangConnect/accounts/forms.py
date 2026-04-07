from django import forms
from .models import Donneur, Hopital

class InscriptionDonneurForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur")
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    first_name = forms.CharField(label="Prénom")
    last_name = forms.CharField(label="Nom")
    groupe_sanguin = forms.ChoiceField(choices=[
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ])
    sexe = forms.ChoiceField(choices=[('M', 'Masculin'), ('F', 'Féminin')])
    date_naissance = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    ville = forms.CharField(max_length=100)
    telephone = forms.CharField(max_length=20, required=False)


class InscriptionHopitalForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur")
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    nom = forms.CharField(max_length=200)
    adresse = forms.CharField(widget=forms.Textarea)
    ville = forms.CharField(max_length=100)
    telephone = forms.CharField(max_length=20)
    agrement = forms.CharField(max_length=50)