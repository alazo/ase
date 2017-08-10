import json

from django.views.generic import DetailView, ListView, TemplateView
from django.http import HttpResponse
from django.db.models import F, Sum

from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.colors import HexColor

from .forms import CoursProfAdminForm
from .models import (Competence, ObjectifParticulier, 
                     ObjectifEvaluateur, Domaine, Cours, Document)
from pdf.models import PDFResponse, MyDocTemplateLandscape


class HomeViewFE(ListView):
    model = Domaine
    template_name = 'pec/index_fe.html'
    
    def get_queryset(self):
        return Domaine.objects.all().exclude(abrev='CIE')


class HomeViewMP(ListView):
    model = Domaine
    template_name = 'pec/index_mp.html'
    
    def get_queryset(self):
        return Domaine.objects.all().exclude(abrev='ECG').exclude(abrev='EPH')
    
    
class CompetenceProfView(DetailView):
    model = Competence
    template_name = 'pec/comp_prof_detail.html'
    exclude = ('tri',)

    
class CompetenceMethoView(DetailView):
    model = Competence
    template_name = 'pec/comp_metho_detail.html'


class CoursDetailView(DetailView):
    model = Cours
    template_name = 'pec/cours_detail.html'


class CompetencePersoView(DetailView):
    model = Competence
    template_name = 'pec/comp_perso_detail.html'


class CompetenceProfListView(ListView):
    model = Competence
    template_name = 'pec/comp_prof_liste.html'


class ObjectifParticulierListView(ListView):
    model = ObjectifParticulier
    template_name = 'pec/obj_eval_liste.html'
        
    def get_queryset(self):
        return ObjectifParticulier.objects.all()

    
class PeriodeView(TemplateView):
    template_name = 'pec/periode.html'
    
    def get_context_data(self, **kwargs):
        context = super(PeriodeView, self).get_context_data(**kwargs) 
        filiere = self.kwargs['filiere']
        if filiere == 'MP':
            context['cours1'] = Cours.objects.filter(cursus__code='1MP').exclude(index_published=False)
            context['cours2'] = Cours.objects.filter(cursus__code='2MP').exclude(index_published=False)
            context['cours3'] = Cours.objects.filter(cursus__code='3MP').exclude(index_published=False)
            context['toggle'] = 'MP'
            context['formation'] = 'Formation avec matu. prof. intégrée'
        if filiere == 'FE':
            context['cours1'] = Cours.objects.filter(cursus__code='1FE').exclude(index_published=False)
            context['cours2'] = Cours.objects.filter(cursus__code='2FE').exclude(index_published=False)
            context['cours3'] = Cours.objects.filter(cursus__code='3FE').exclude(index_published=False)
            context['toggle'] = 'FE'
            context['formation'] = 'Formation en entreprise'
            
        context['tot1'] = context['cours1'].aggregate(Sum(F('periode')))['periode__sum'] 
        context['tot2'] = context['cours2'].aggregate(Sum(F('periode')))['periode__sum'] 
        context['tot3'] = context['cours3'].aggregate(Sum(F('periode')))['periode__sum'] 
        context['tot'] = context['tot1'] + context['tot2'] + context['tot3']
        return context   
    
    
class PeriodeDomaineView(ListView):
    model = Domaine
    template_name = 'pec/periode_domaine.html'
    
    def get_context_data(self, **kwargs):
        filiere = self.kwargs['filiere']
        context = super(PeriodeDomaineView, self).get_context_data(**kwargs)
        if filiere == 'MP':
            exclude_fields = ['ECG', 'EPH']
            c1 = Cours.objects.filter(cursus__code='1MP').exclude(index_published=False)
            c2 = Cours.objects.filter(cursus__code='2MP').exclude(index_published=False)
            c3 = Cours.objects.filter(cursus__code='3MP').exclude(index_published=False)
            context['formation'] = 'Formation avec matu. prof. intégrée'
            context['toggle'] = 'MP'
        if filiere == 'FE':
            exclude_fields = ['CIE']
            c1 = Cours.objects.filter(cursus__code='1FE').exclude(index_published=False)
            c2 = Cours.objects.filter(cursus__code='2FE').exclude(index_published=False)
            c3 = Cours.objects.filter(cursus__code='3FE').exclude(index_published=False)
            context['formation'] = 'Formation en entreprise'
            context['toggle'] = 'FE'
        
        dom = []
        for i, d in enumerate(Domaine.objects.all().exclude(abrev__in=exclude_fields)):              
            d.tot1 = c1.filter(domaine=d).aggregate(Sum(F('periode')))['periode__sum']
            d.tot2 = c2.filter(domaine=d).aggregate(Sum(F('periode')))['periode__sum']
            d.tot3 = c3.filter(domaine=d).aggregate(Sum(F('periode')))['periode__sum'] 
            dom.append(d)
        
        context['dom'] = dom
        context['a1'] = c1.aggregate(Sum(F('periode')))['periode__sum']
        context['a2'] = c2.aggregate(Sum(F('periode')))['periode__sum']
        context['a3'] = c3.aggregate(Sum(F('periode')))['periode__sum']
        context['aa'] = context['a1'] + context['a2'] + context['a3']
        return context

             
class SeminaireView(TemplateView):
    template_name = 'pec/seminaire.html'
    

class CoursFEListView(ListView):
    model = Cours
    template_name = 'pec/cours.html'    
    
    def get_queryset(self):
        return Cours.objects.all().order_by('nom')    


class CoursAdminView(DetailView):
    model = Cours
    template_name = 'pec/cours_admin.html'
    form_class = CoursProfAdminForm
    
    def get_context_data(self, **kwargs):
        context = super(CoursAdminView, self).get_context_data(**kwargs)
        context['form'] = CoursProfAdminForm   
        return context


class DocumentListView(ListView):
    model = Document
    # template_name = 'pec/document_list.html'
    
    def get_queryset(self):
        return Document.objects.filter(published=True)


class DocumentDetailView(DetailView):
    model = Document
    template_name = 'pec/document_detail.html'
    
    
def plan_form_pdf(filiere):
    """Retourne le pdf du plan de formation FE"""
    table_style = []
    story = [['Domaine', 'Année1', 'Année 2', 'Année 3']]
    
    if filiere == 'FE':
        domaines = Domaine.objects.exclude(abrev='CIE')
        response = PDFResponse('PlanFormation.pdf', 'Plan de formation FE', portrait=False)
            
        for row, d in enumerate(domaines):
            c1 = '\n'.join('{0} ({1} pér.)'.format(x.nom, x.periode) for x in d.cours_fe_annee_1)
            c2 = '\n'.join('{0} ({1} pér.)'.format(x.nom, x.periode) for x in d.cours_fe_annee_2())
            c3 = '\n'.join('{0} ({1} pér.)'.format(x.nom, x.periode) for x in d.cours_fe_annee_3())
            story.append([d.nom, c1, c2, c3])
            color = '{0}'.format(d.couleur[:7])
            table_style.append(('BACKGROUND', (0, row+1), (3, row+1), HexColor(color)),)
    else:
        domaines = Domaine.objects.all().exclude(abrev='ECG').exclude(abrev='EPH')
        response = PDFResponse('PlanFormation.pdf', 'Plan de formation MPI', portrait=False)
        for row, d in enumerate(domaines):
            c1 = '\n'.join('{0} ({1} pér.)'.format(x.nom, x.periode) for x in d.cours_mp_annee_1())
            c2 = '\n'.join('{0} ({1} pér.)'.format(x.nom, x.periode) for x in d.cours_mp_annee_2())
            c3 = '\n'.join('{0} ({1} pér.)'.format(x.nom, x.periode) for x in d.cours_mp_annee_3())
            story.append([d.nom, c1, c2, c3])
            color = '{0}'.format(d.couleur[:7])
            table_style.append(('BACKGROUND', (0, row+1), (3, row+1), HexColor(color)),)

    t = Table(story, colWidths=[6.5*cm, 6.5*cm, 6.5*cm, 6.5*cm], spaceBefore=0.5*cm, spaceAfter=1*cm)
    table_style.extend([
        ('SIZE', (0, 0), (-1, -1), 7),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black)])

    t.setStyle(TableStyle(table_style))
                           
    response.story.append(t)
    doc = MyDocTemplateLandscape(response)  
    doc.build(response.story)
    return response
    

def json_objeval(pk):
    """Retourne les objectifs évaluateurs de l'obj. particulier PK
       et filtre sur les orientation Global et Gén uniquement
    """
    objs = ObjectifEvaluateur.objects.filter(objectif_particulier=pk).filter(orientation__lte=2)
    data = [{'code': o.code,
             'orientation': o.orientation.nom,
             'nom': o.nom,
             'taxonomie': o.taxonomie.code} for o in objs]
    return HttpResponse(json.dumps(data), content_type="application/json")
