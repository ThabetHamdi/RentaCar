from django.db import models
from django.contrib import admin


class Voiture(models.Model):
    num_imma = models.CharField(max_length=20, unique=True)  # Numéro d'immatriculation unique
    marque = models.CharField(max_length=50)
    modele = models.CharField(max_length=50)
    kilometrage = models.IntegerField()
    etat = models.BooleanField(default=True)  # True = Disponible, False = Louée
    prix_location = models.FloatField()
    image = models.ImageField(upload_to='voitures/', blank=True, null=True)  # Champ image

    def __str__(self):
        return f"{self.marque} {self.modele} ({'Disponible' if self.etat else 'Louée'})"


class Locataire(models.Model):
    id_loc = models.AutoField(primary_key=True)  # Auto-incremented ID
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    adresse = models.TextField()

    def __str__(self):
        return f"{self.nom} {self.prenom}"


class Location(models.Model):
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE)
    locataire = models.ForeignKey(Locataire, on_delete=models.CASCADE)
    date_debut = models.DateField(auto_now_add=True)
    date_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.voiture} louée par {self.locataire} du {self.date_debut} au {self.date_fin or 'En cours'}"
