from django.contrib import admin

from .models import (Domaine, Competence, ObjectifParticulier, ObjectifEvaluateur,
                     Orientation, Taxonomie, CompetenceTransversale,
                     Cursus, Cours)
from .forms import ObjectifParticulierAdminForm
# Register your models here.


class DomainAdmin(admin.ModelAdmin):
    pass

class ObjectifEvaluateurAdmin(admin.ModelAdmin):
    list_display = ('code', 'orientation', 'nom', 'objectif_particulier')
    

class ObjectifParticulierAdmin(admin.ModelAdmin):
    model = ObjectifParticulier
    form = ObjectifParticulierAdminForm   


    
admin.site.register(Orientation)
admin.site.register(Taxonomie)

admin.site.register(Domaine)
admin.site.register(Competence)
admin.site.register(ObjectifParticulier, ObjectifParticulierAdmin)
admin.site.register(ObjectifEvaluateur, ObjectifEvaluateurAdmin)
admin.site.register(CompetenceTransversale)
admin.site.register(Cursus)
admin.site.register(Cours)