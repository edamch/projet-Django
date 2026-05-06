from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
import csv
from accounts.models import Donneur, Hopital
from hopitaux.models import DemandeUrgente
from .forms import InscriptionDonneurForm, InscriptionHopitalForm
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from donneurs.models import Don, ReponseAppel
from hopitaux.models import DemandeUrgente

def inscription_donneur(request):
    if request.method == 'POST':
        form = InscriptionDonneurForm(request.POST)
        if form.is_valid():

            if User.objects.filter(username=form.cleaned_data['username']).exists():
                messages.error(request, "Ce nom d'utilisateur est déjà pris.")
                return render(request, 'accounts/inscription_donneur.html', {'form': form})


            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            Donneur.objects.create(
                user=user,
                groupe_sanguin=form.cleaned_data['groupe_sanguin'],
                sexe=form.cleaned_data['sexe'],
                date_naissance=form.cleaned_data['date_naissance'],
                ville=form.cleaned_data['ville'],
                telephone=form.cleaned_data['telephone'],
            )
            messages.success(request, "Compte créé avec succès !")
            return redirect('login')
    else:
        form = InscriptionDonneurForm()
    return render(request, 'accounts/inscription_donneur.html', {'form': form})

def inscription_hopital(request):
    if request.method == 'POST':
        form = InscriptionHopitalForm(request.POST)
        if form.is_valid():

            # Vérifier si le username existe déjà
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                messages.error(request, "Ce nom d'utilisateur est déjà pris.")
                return render(request, 'accounts/inscription_hopital.html', {'form': form})

            # Vérifier si l'agrément existe déjà
            if Hopital.objects.filter(agrement=form.cleaned_data['agrement']).exists():
                messages.error(request, "Ce numéro d'agrément est déjà utilisé.")
                return render(request, 'accounts/inscription_hopital.html', {'form': form})

            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            Hopital.objects.create(
                user=user,
                nom=form.cleaned_data['nom'],
                adresse=form.cleaned_data['adresse'],
                ville=form.cleaned_data['ville'],
                telephone=form.cleaned_data['telephone'],
                agrement=form.cleaned_data['agrement'],
            )
            messages.success(request, "Demande envoyée, en attente de validation.")
            return redirect('login')
    else:
        form = InscriptionHopitalForm()
    return render(request, 'accounts/inscription_hopital.html', {'form': form})


def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # Rediriger selon le rôle
            if hasattr(user, 'donneur'):
                return redirect('donneur_dashboard')
            elif hasattr(user, 'hopital'):
                return redirect('hopital_dashboard')
            else:
                return redirect('admin:index')
        else:
            messages.error(request, "Identifiants incorrects.")
    return render(request, 'accounts/login.html')


def deconnexion(request):
    logout(request)
    return redirect('login')

def accueil(request):
    return render(request, 'accounts/accueil.html')

@staff_member_required
def admin_dashboard(request):
    total_donneurs = Donneur.objects.count()
    total_dons = Don.objects.count()
    total_hopitaux = Hopital.objects.count()
    hopitaux_en_attente = Hopital.objects.filter(valide=False)
    groupes = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    demandes_par_groupe = []
    for groupe in groupes:
        count = DemandeUrgente.objects.filter(
            statut='active',
            groupe_sanguin=groupe
        ).count()
        demandes_par_groupe.append({'groupe': groupe, 'count': count})

    demandes_par_ville = DemandeUrgente.objects.filter(
        statut='active'
    ).values('hopital__ville').annotate(total=Count('id'))

    return render(request, 'accounts/admin_dashboard.html', {
        'total_donneurs': total_donneurs,
        'total_dons': total_dons,
        'total_hopitaux': total_hopitaux,
        'hopitaux_en_attente': hopitaux_en_attente,
        'demandes_par_groupe': demandes_par_groupe,
        'demandes_par_ville': demandes_par_ville,
    })


@staff_member_required
def valider_hopital(request, hopital_id):
    hopital = get_object_or_404(Hopital, id=hopital_id)
    hopital.valide = True
    hopital.save()
    messages.success(request, f"{hopital.nom} validé avec succès !")
    return redirect('admin_dashboard')


@staff_member_required
def export_csv_donneurs(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="donneurs.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nom', 'Prénom', 'Email', 'Groupe Sanguin', 'Ville', 'Téléphone', 'Actif'])

    for donneur in Donneur.objects.all():
        writer.writerow([
            donneur.user.last_name,
            donneur.user.first_name,
            donneur.user.email,
            donneur.groupe_sanguin,
            donneur.ville,
            donneur.telephone,
            donneur.actif,
        ])

    return response