from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DemandeUrgente
from accounts.models import Hopital

@login_required
def hopital_dashboard(request):
    hopital = get_object_or_404(Hopital, user=request.user)
    demandes = DemandeUrgente.objects.filter(hopital=hopital)
    return render(request, 'hopitaux/dashboard.html', {'hopital': hopital, 'demandes': demandes})

@login_required
def publier_demande(request):
    hopital = get_object_or_404(Hopital, user=request.user)

    if not hopital.valide:
        messages.error(request, "Votre compte n'est pas encore validé par l'administrateur.")
        return redirect('hopital_dashboard')

    if request.method == 'POST':
        DemandeUrgente.objects.create(
            hopital=hopital,
            groupe_sanguin=request.POST['groupe_sanguin'],
            quantite=request.POST['quantite'],
            delai=request.POST['delai'],
            description=request.POST['description'],
        )
        messages.success(request, "Demande publiée avec succès !")
        return redirect('hopital_dashboard')

    return render(request, 'hopitaux/publier_demande.html')

@login_required
def cloturer_demande(request, demande_id):
    demande = get_object_or_404(DemandeUrgente, id=demande_id)
    demande.statut = 'cloturee'
    demande.save()
    messages.success(request, "Demande clôturée.")
    return redirect('hopital_dashboard')