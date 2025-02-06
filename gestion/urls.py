from django.urls import path
from .views import (
    liste_voitures, ajouter_voiture, modifier_voiture, supprimer_voiture,
    liste_locataires, ajouter_locataire, modifier_locataire, supprimer_locataire,
    liste_locations, louer_voiture, rendre_voiture, supprimer_location
)

urlpatterns = [
    # Voitures URLs
    path('voitures/', liste_voitures, name='liste_voitures'),
    path('voitures/ajouter/', ajouter_voiture, name='ajouter_voiture'),
    path('voitures/modifier/<int:id>/', modifier_voiture, name='modifier_voiture'),
    path('voitures/supprimer/<int:id>/', supprimer_voiture, name='supprimer_voiture'),

    # Locataires URLs
    path('locataires/', liste_locataires, name='liste_locataires'),
    path('locataires/ajouter/', ajouter_locataire, name='ajouter_locataire'),
    path('locataires/modifier/<int:id>/', modifier_locataire, name='modifier_locataire'),
    path('locataires/supprimer/<int:id>/', supprimer_locataire, name='supprimer_locataire'),

    # Locations URLs
    path('locations/', liste_locations, name='liste_locations'),
    path('locations/louer/', louer_voiture, name='louer_voiture'),
    path('locations/rendre/<int:id>/', rendre_voiture, name='rendre_voiture'),
    path('locations/supprimer/<int:id>/', supprimer_location, name='supprimer_location'),
]


from .views import home

urlpatterns += [
    path('', home, name='home'),  # Home Dashboard
]


from .views import (
    exporter_voitures_pdf, exporter_locataires_pdf, exporter_locations_pdf
)

urlpatterns += [
    path('voitures/export/pdf/', exporter_voitures_pdf, name='exporter_voitures_pdf'),
    path('locataires/export/pdf/', exporter_locataires_pdf, name='exporter_locataires_pdf'),
    path('locations/export/pdf/', exporter_locations_pdf, name='exporter_locations_pdf'),
]
