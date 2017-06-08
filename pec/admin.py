from django.contrib import admin

from .models import (Domaine, Competence, ObjectifParticulier, ObjectifEvaluateur,
                     Orientation, Taxonomie, CompetenceTransversale,
                     Cursus, Cours, TypeCompetence, Sequence, Document)
from .forms import ObjectifParticulierAdminForm, CoursAdminForm, DocumentAdminForm
# Register your models here.


class DomainAdmin(admin.ModelAdmin):
    pass

class ObjectifEvaluateurAdmin(admin.ModelAdmin):
    search_fields = ('nom',)
    list_display = ('code', 'orientation', 'nom', 'taxonomie')
    
    list_filter = ('orientation',)
    
    class Meta:
        ordering = ('tri',)


class ObjectifParticulierAdmin(admin.ModelAdmin):
    model = ObjectifParticulier
    form = ObjectifParticulierAdminForm   


class SequenceAdmin(admin.ModelAdmin):
    pass

     
class SequenceInline(admin.TabularInline):
    fields = ('titre', 'cours' )
    model = Sequence
    extra = 0
    
        
class CoursAdmin(admin.ModelAdmin):
    list_display = ('nom', 'periode', 'careum', 'cursus_txt', 'domaine')
    exclude = ('objectifs_evaluateurs',)
    list_filter = ('cursus', 'domaine')
    inlines = [SequenceInline, ]
    form = CoursAdminForm

    
class DocumentAdmin(admin.ModelAdmin):
    form = DocumentAdminForm
       
    
admin.site.register(Orientation)
admin.site.register(Taxonomie)

admin.site.register(Domaine)
admin.site.register(Competence)
admin.site.register(ObjectifParticulier, ObjectifParticulierAdmin)
admin.site.register(ObjectifEvaluateur, ObjectifEvaluateurAdmin)
admin.site.register(CompetenceTransversale)
admin.site.register(Cursus)
admin.site.register(Cours, CoursAdmin)
admin.site.register(TypeCompetence)
admin.site.register(Sequence, SequenceAdmin)
admin.site.register(Document, DocumentAdmin)