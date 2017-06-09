# -*- encoding: utf-8 -*-
'''
Created on 17 nov. 2012

@author: alzo
'''
import os
from django import forms
from .models import Cours, Document
from django.core.exceptions import ValidationError

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

class SequenceInlineAdminForm(forms.ModelForm):
          
    class Meta:
        widgets = {
                'contenu': forms.Textarea(attrs={'cols': 40, 'rows':2}),
                'objectifs_apprentissage': forms.Textarea(attrs={'cols': 40, 'rows':2}),
                'objectifs_evaluateurs_txt': forms.TextInput(attrs={'size':10}),
                'careum': forms.TextInput(attrs={'size':10}),
            } 
        
        
class CoursAdminForm(forms.ModelForm):
    
    class Meta:
        model = Cours
        
        fields = ('nom', 'descr','type', 'periode', 'nbre_note', 'domaine',
                  'careum', 'cursus_txt', 'index_published',
                  'didactique','evaluation')
        
        widgets = {
            'descr': forms.Textarea(attrs={'cols': 80, 'rows':2}),
            }
        
class DocumentAdminForm(forms.ModelForm):
    
    class Meta:
        model = Document
        fields = ('titre', 'path', 'published', )   
    
    def clean(self):
        cleaned_data = super(DocumentAdminForm, self).clean()
        data = cleaned_data.get("path")
        ext_whitelist = ['pdf']
        ext = data.name[-3:].lower()
        
        if ext not in ext_whitelist:
            raise forms.ValidationError("Seuls les fichiers PDF sont autorisés !")