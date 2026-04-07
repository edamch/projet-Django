from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import InscriptionDonneurForm, InscriptionHopitalForm

def inscription_donneur(request):
    if request.method == 'POST':
        form = InscriptionDonneurForm(request.POST)
        if form.is_valid():
            # Créer le User
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            # Créer le profil Donneur
            donneur = form.save(commit=False)
            donneur.user = user
            donneur.save()
            messages.success(request, "Compte créé avec succès !")
            return redirect('login')
    else:
        form = InscriptionDonneurForm()
    return render(request, 'accounts/inscription_donneur.html', {'form': form})


def inscription_hopital(request):
    if request.method == 'POST':
        form = InscriptionHopitalForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            hopital = form.save(commit=False)
            hopital.user = user
            hopital.save()
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