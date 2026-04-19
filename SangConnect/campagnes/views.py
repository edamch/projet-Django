from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Campagne, Inscription
from accounts.models import Hopital, Donneur

@login_required
def liste_campagnes(request):
    campagnes = Campagne.objects.filter(date__gte=__import__('datetime').date.today())
    return render(request, 'campagnes/liste.html', {'campagnes': campagnes})

@login_required
def creer_campagne(request):
    hopital = get_object_or_404(Hopital, user=request.user)

    if request.method == 'POST':
        Campagne.objects.create(
            hopital=hopital,
            nom=request.POST['nom'],
            date=request.POST['date'],
            lieu=request.POST['lieu'],
            groupes_cibles=request.POST['groupes_cibles'],
            capacite_totale=request.POST['capacite_totale'],
            description=request.POST.get('description', ''),
        )
        messages.success(request, "Campagne créée avec succès !")
        return redirect('hopital_dashboard')

    return render(request, 'campagnes/creer.html')

@login_required
def inscrire_campagne(request, campagne_id):
    donneur = get_object_or_404(Donneur, user=request.user)
    campagne = get_object_or_404(Campagne, id=campagne_id)

    # Vérifier capacité
    if campagne.places_restantes() <= 0:
        messages.error(request, "Cette campagne est complète.")
        return redirect('liste_campagnes')

    # Vérifier si déjà inscrit
    deja_inscrit = Inscription.objects.filter(donneur=donneur, campagne=campagne).exists()
    if deja_inscrit:
        messages.warning(request, "Vous êtes déjà inscrit à cette campagne.")
        return redirect('liste_campagnes')

    if request.method == 'POST':
        Inscription.objects.create(
            donneur=donneur,
            campagne=campagne,
            creneau_horaire=request.POST['creneau_horaire'],
        )
        messages.success(request, "Inscription confirmée !")
        return redirect('donneur_dashboard')

    return render(request, 'campagnes/inscrire.html', {'campagne': campagne})