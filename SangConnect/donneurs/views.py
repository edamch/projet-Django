from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import Donneur
from hopitaux.models import DemandeUrgente
from .models import Don, ReponseAppel
from datetime import date

# Tableau de compatibilité des groupes sanguins
COMPATIBILITE = {
    'A+':  ['A+', 'A-', 'O+', 'O-'],
    'A-':  ['A-', 'O-'],
    'B+':  ['B+', 'B-', 'O+', 'O-'],
    'B-':  ['B-', 'O-'],
    'AB+': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
    'AB-': ['A-', 'B-', 'AB-', 'O-'],
    'O+':  ['O+', 'O-'],
    'O-':  ['O-'],
}

@login_required
def donneur_dashboard(request):
    donneur = get_object_or_404(Donneur, user=request.user)
    dons = Don.objects.filter(donneur=donneur)

    # Demandes compatibles avec le groupe sanguin du donneur
    groupes_compatibles = COMPATIBILITE.get(donneur.groupe_sanguin, [])
    demandes = DemandeUrgente.objects.filter(
        statut='active',
        groupe_sanguin__in=groupes_compatibles
    )

    return render(request, 'donneurs/dashboard.html', {
        'donneur': donneur,
        'dons': dons,
        'demandes': demandes,
        'prochaine_date': donneur.prochaine_date_don(),
        'eligible': donneur.est_eligible(),
    })

@login_required
def repondre_appel(request, demande_id):
    donneur = get_object_or_404(Donneur, user=request.user)
    demande = get_object_or_404(DemandeUrgente, id=demande_id)

    if not donneur.est_eligible():
        messages.error(request, f"Vous n'êtes pas éligible avant le {donneur.prochaine_date_don()}.")
        return redirect('donneur_dashboard')

    # Vérifier si déjà répondu
    deja_repondu = ReponseAppel.objects.filter(donneur=donneur, demande=demande).exists()
    if deja_repondu:
        messages.warning(request, "Vous avez déjà répondu à cet appel.")
        return redirect('donneur_dashboard')

    ReponseAppel.objects.create(donneur=donneur, demande=demande)
    messages.success(request, "Votre intention de don a été enregistrée !")
    return redirect('donneur_dashboard')

@login_required
def enregistrer_don(request):
    donneur = get_object_or_404(Donneur, user=request.user)

    if not donneur.est_eligible():
        messages.error(request, f"Vous n'êtes pas éligible avant le {donneur.prochaine_date_don()}.")
        return redirect('donneur_dashboard')

    if request.method == 'POST':
        Don.objects.create(
            donneur=donneur,
            hopital_id=request.POST['hopital'],
            date_don=request.POST['date_don'],
            notes=request.POST.get('notes', ''),
        )
        messages.success(request, "Don enregistré avec succès !")
        return redirect('donneur_dashboard')

    from accounts.models import Hopital
    hopitaux = Hopital.objects.filter(valide=True)
    return render(request, 'donneurs/enregistrer_don.html', {'hopitaux': hopitaux})