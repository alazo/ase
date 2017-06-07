import json
from django.views.generic import DetailView, ListView, TemplateView
# Create your views here.
from .forms import CoursProfAdminForm
from .models import (Competence, ObjectifParticulier, 
                     ObjectifEvaluateur, Domaine, Cours)
from django.http import HttpResponse
from django.db.models import F, Sum
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait, landscape
from reportlab.lib.units import cm


def TriOPar(self):
    """Renseigne un champ permettant le tri"""
    
    for op in ObjectifParticulier.objects.all():
        src = op.code.split('.')
        op.tri = int(src[0])* 100 + int(src[1])
        op.save()

  
def TriOEva(self):
    """Renseigne un champ permettant le tri"""
    for op in ObjectifEvaluateur.objects.all():
        src = op.code.split('.')
        op.tri = int(src[0]) * 10000 + int(src[1])* 100 + int(src[2])
        op.save()
        
        
class HomeViewFE(ListView):
    model = Domaine
    template_name = 'pec/index_fe.html'
    
    def get_queryset(self):
        return Domaine.objects.all().exclude(abrev='CIE')

   
class HomeViewMP(ListView):
    model = Domaine
    template_name = 'pec/index_mp.html'
    
    def get_queryset(self):
        return Domaine.objects.all().exclude(abrev='ECG').exclude(abrev= 'EPH')
    
    
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
    
    """
    def get_queryset(self):
        return Domaine.objects.all().exclude(abrev='CIE')
    """
    
    
    """
    def get_context_data(self, **kwargs):
        context = super(CoursDetailView, self).get_context_data(**kwargs)   
        context['eval'] = self.object.objectifs_evaluateurs.all()
        return context
    """
    
    
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



class PeriodeFEView(TemplateView):
    template_name = 'pec/periode_fe.html'
    
    def get_context_data(self, **kwargs):
        context = super(PeriodeFEView, self).get_context_data(**kwargs)   
        context['cours1'] = Cours.objects.filter(cursus__code='1FE').exclude(index_published=False)
        context['cours2'] = Cours.objects.filter(cursus__code='2FE').exclude(index_published=False)
        context['cours3'] = Cours.objects.filter(cursus__code='3FE').exclude(index_published=False)
    
        context['tot1'] = context['cours1'].aggregate(Sum(F('periode')))['periode__sum'] 
        context['tot2'] = context['cours2'].aggregate(Sum(F('periode')))['periode__sum'] 
        context['tot3'] = context['cours3'].aggregate(Sum(F('periode')))['periode__sum'] 
        context['tot'] = context['tot1'] + context['tot2'] + context['tot3']
        return context

    
class PeriodeMPView(TemplateView):
    template_name = 'pec/periode_mp.html'
    
    def get_context_data(self, **kwargs):
        context = super(PeriodeMPView, self).get_context_data(**kwargs)   
        context['cours1'] = Cours.objects.filter(cursus__code='1MP').exclude(index_published=False)
        context['cours2'] = Cours.objects.filter(cursus__code='2MP').exclude(index_published=False)
        context['cours3'] = Cours.objects.filter(cursus__code='3MP').exclude(index_published=False)
        context['tot1'] = context['cours1'].aggregate(Sum(F('periode')))['periode__sum'] 
        context['tot2'] = context['cours2'].aggregate(Sum(F('periode')))['periode__sum'] 
        context['tot3'] = context['cours3'].aggregate(Sum(F('periode')))['periode__sum'] 
        context['tot'] = context['tot1'] + context['tot2'] + context['tot3']
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

    
def plan_form_fe_pdf(request): 
    from io import StringIO
    from xhtml2pdf import pisa
    from django.template.loader import get_template
    from django.template import Context
    from django.http import HttpResponse
    from cgi import escape
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    
    context_dict = Domaine.objects.all().exclude(abrev='CIE')
    template = 'pec/index-fe.html'
    context = Context({'object_list': context_dict})
    html  = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
               
        

def json_objeval(request, pk):
    """Retourne les objectifs évaluateurs de l'obj. particulier PK
       et filtre sur les orientation Global et Gén uniquement
    """
    objs = ObjectifEvaluateur.objects.filter(objectif_particulier=pk).filter(orientation__lte=2)
    
    data =[{'code': o.code, 'orientation':o.orientation.nom, 'nom':o.nom, 'taxonomie':o.taxonomie.code} for o in objs]
    
    return HttpResponse(json.dumps(data), content_type="application/json")
    