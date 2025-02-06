from django.contrib import admin
from .models import Voiture

class VoitureAdmin(admin.ModelAdmin):
    list_display = ('num_imma', 'marque', 'modele', 'etat', 'prix_location', 'image_display')

    def image_display(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50" />'
        return "Pas d'image"
    
    image_display.allow_tags = True
    image_display.short_description = "Aperçu"

admin.site.register(Voiture, VoitureAdmin)



from .models import Locataire

class LocataireAdmin(admin.ModelAdmin):
    list_display = ('id_loc', 'nom', 'prenom', 'adresse')
    search_fields = ('nom', 'prenom')

admin.site.register(Locataire, LocataireAdmin)
