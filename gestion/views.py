from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Voiture, Locataire, Location
from .forms import VoitureForm, LocataireForm, LocationForm

# -------------------------------
# 🔹 Gestion des Voitures
# -------------------------------

def liste_voitures(request):
    query = request.GET.get('q')
    filter_status = request.GET.get('status')

    voitures = Voiture.objects.all()

    if query:
        voitures = voitures.filter(
            Q(marque__icontains=query) |
            Q(modele__icontains=query) |
            Q(num_imma__icontains=query)
        )

    if filter_status == "disponible":
        voitures = voitures.filter(etat=True)
    elif filter_status == "louee":
        voitures = voitures.filter(etat=False)

    # PAGINATION (5 voitures par page)
    paginator = Paginator(voitures, 5)  
    page_number = request.GET.get('page')
    voitures_page = paginator.get_page(page_number)

    return render(request, 'gestion/liste_voitures.html', {'voitures': voitures_page})

def ajouter_voiture(request):
    if request.method == "POST":
        form = VoitureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('liste_voitures')
    else:
        form = VoitureForm()
    return render(request, 'gestion/ajouter_voiture.html', {'form': form})

def modifier_voiture(request, id):
    voiture = get_object_or_404(Voiture, id=id)
    if request.method == "POST":
        form = VoitureForm(request.POST, request.FILES, instance=voiture)
        if form.is_valid():
            form.save()
            return redirect('liste_voitures')
    else:
        form = VoitureForm(instance=voiture)
    return render(request, 'gestion/modifier_voiture.html', {'form': form})

def supprimer_voiture(request, id):
    voiture = get_object_or_404(Voiture, id=id)
    if request.method == "POST":
        voiture.delete()
        return redirect('liste_voitures')
    return render(request, 'gestion/supprimer_voiture.html', {'voiture': voiture})


# -------------------------------
# 🔹 Gestion des Locataires
# -------------------------------

def liste_locataires(request):
    query = request.GET.get('q')
    locataires = Locataire.objects.all()

    if query:
        locataires = locataires.filter(
            Q(nom__icontains=query) | 
            Q(prenom__icontains=query)
        )

    # PAGINATION (5 locataires par page)
    paginator = Paginator(locataires, 5)  
    page_number = request.GET.get('page')
    locataires_page = paginator.get_page(page_number)

    return render(request, 'gestion/liste_locataires.html', {'locataires': locataires_page})

def ajouter_locataire(request):
    if request.method == "POST":
        form = LocataireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_locataires')
    else:
        form = LocataireForm()
    return render(request, 'gestion/ajouter_locataire.html', {'form': form})

def modifier_locataire(request, id):
    locataire = get_object_or_404(Locataire, id_loc=id)
    if request.method == "POST":
        form = LocataireForm(request.POST, instance=locataire)
        if form.is_valid():
            form.save()
            return redirect('liste_locataires')
    else:
        form = LocataireForm(instance=locataire)
    return render(request, 'gestion/modifier_locataire.html', {'form': form})

def supprimer_locataire(request, id):
    locataire = get_object_or_404(Locataire, id_loc=id)
    if request.method == "POST":
        locataire.delete()
        return redirect('liste_locataires')
    return render(request, 'gestion/supprimer_locataire.html', {'locataire': locataire})


# -------------------------------
# 🔹 Gestion des Locations
# -------------------------------

def liste_locations(request):
    query = request.GET.get('q')
    locations = Location.objects.all()

    if query:
        locations = locations.filter(
            Q(locataire__nom__icontains=query) |
            Q(voiture__marque__icontains=query) |
            Q(voiture__modele__icontains=query)
        )

    # PAGINATION (5 locations par page)
    paginator = Paginator(locations, 5)  
    page_number = request.GET.get('page')
    locations_page = paginator.get_page(page_number)

    return render(request, 'gestion/liste_locations.html', {'locations': locations_page})

def louer_voiture(request):
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)

            # Vérifier si la voiture est déjà louée
            if not location.voiture.etat:
                return render(request, 'gestion/louer_voiture.html', {
                    'form': form,
                    'error': "Cette voiture est déjà louée !"
                })

            location.voiture.etat = False  # Marquer la voiture comme louée
            location.voiture.save()
            location.save()
            return redirect('liste_locations')

    else:
        form = LocationForm()
    return render(request, 'gestion/louer_voiture.html', {'form': form})

def rendre_voiture(request, id):
    location = get_object_or_404(Location, id=id)

    if request.method == "POST":
        date_fin = request.POST.get('date_fin')

        if not date_fin:
            return render(request, 'gestion/rendre_voiture.html', {
                'location': location,
                'error': "Veuillez indiquer une date de retour."
            })

        location.date_fin = date_fin  # Met à jour la date de fin
        location.voiture.etat = True  # Marque la voiture comme disponible
        location.voiture.save()
        location.save()
        return redirect('liste_locations')

    return render(request, 'gestion/rendre_voiture.html', {'location': location})


def supprimer_location(request, id):
    location = get_object_or_404(Location, id=id)
    if request.method == "POST":
        location.delete()
        return redirect('liste_locations')
    return render(request, 'gestion/supprimer_location.html', {'location': location})


# -------------------------------
# 🔹 Dashboard / Accueil
# -------------------------------

def home(request):
    total_voitures = Voiture.objects.count()
    voitures_dispo = Voiture.objects.filter(etat=True).count()
    voitures_louees = total_voitures - voitures_dispo
    total_locataires = Locataire.objects.count()
    locations_actives = Location.objects.filter(date_fin__isnull=True).count()

    context = {
        'total_voitures': total_voitures,
        'voitures_dispo': voitures_dispo,
        'voitures_louees': voitures_louees,
        'total_locataires': total_locataires,
        'locations_actives': locations_actives,
    }
    return render(request, 'gestion/home.html', context)



from django.http import HttpResponse
from reportlab.pdfgen import canvas

def exporter_voitures_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="voitures.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica", 14)
    p.drawString(100, 800, "Liste des Voitures")

    voitures = Voiture.objects.all()
    y_position = 780  # Position initiale du texte

    for voiture in voitures:
        y_position -= 20
        p.drawString(100, y_position, f"{voiture.marque} {voiture.modele} - {voiture.num_imma} - {voiture.kilometrage} km")

    p.showPage()
    p.save()
    return response


def exporter_locataires_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="locataires.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica", 14)
    p.drawString(100, 800, "Liste des Locataires")

    locataires = Locataire.objects.all()
    y_position = 780  

    for locataire in locataires:
        y_position -= 20
        p.drawString(100, y_position, f"{locataire.nom} {locataire.prenom} - {locataire.adresse}")

    p.showPage()
    p.save()
    return response


def exporter_locations_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="locations.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica", 14)
    p.drawString(100, 800, "Liste des Locations")

    locations = Location.objects.all()
    y_position = 780  

    for location in locations:
        y_position -= 20
        p.drawString(100, y_position, f"Voiture: {location.voiture.marque} - {location.voiture.modele}, Loué par: {location.locataire.nom} {location.locataire.prenom}, Début: {location.date_debut}, Fin: {location.date_fin or 'En cours'}")

    p.showPage()
    p.save()
    return response
