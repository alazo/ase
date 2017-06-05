# -*- encoding: utf-8 -*-
'''
Created on 17 nov. 2012

@author: alzo
'''

from django import forms
from .models import Cours

class ObjectifParticulierAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ObjectifParticulierAdminForm, self).__init__(*args, **kwargs)
    
    class Meta:
        
        fields = ('code', 'nom', 'competence', 'competences_transversales')
        widgets = {
            'nom': forms.Textarea(attrs={'cols': 125, 'rows':2}),
            } 


class CoursProfAdminForm(forms.ModelForm):
    
    class Meta:
        model = Cours
        fields = ('nom', 'descr', 'domaine', 'periode', 'nbre_note')
    
    
    def __init__(self, *args, **kwargs):
        super(CoursProfAdminForm, self).__init__(*args, **kwargs)
        