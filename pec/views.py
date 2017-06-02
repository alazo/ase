import json
from django.views.generic import TemplateView, DetailView, ListView
# Create your views here.
from .models import Competence, CompetenceTransversale, ObjectifParticulier, ObjectifEvaluateur
from django.http import HttpResponse

def TriOPar(self):

    for op in ObjectifParticulier.objects.all():
        src = op.code.split('.')
        print(src)
        op.tri = int(src[0])* 100 + int(src[1])
        op.save()
        
def TriOEva(self):

    for op in ObjectifEvaluateur.objects.all():
        src = op.code.split('.')
        op.tri = int(src[0]) * 10000 + int(src[1])* 100 + int(src[2])
        op.save()
        
        
class HomeView(TemplateView):
    template_name = 'pec/index.html'
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)   
        
        context['competences'] = Competence.objects.all()
        context['metho'] = CompetenceTransversale.objects.filter(type=1)
        context['perso'] = CompetenceTransversale.objects.filter(type=2)
        return context

    
class CompetenceProfView(DetailView):
    model = Competence
    template_name = 'pec/comp_prof_detail.html'
    exclude = ('tri',)

    
class CompetenceMethoView(DetailView):
    model = Competence
    template_name = 'pec/comp_metho_detail.html'
    
class CompetencePersoView(DetailView):
    model = Competence
    template_name = 'pec/comp_perso_detail.html'

class CompetenceProfListView(ListView):
    model = Competence
    template_name = 'pec/comp_prof_liste.html'


    
class ObjectifParticulierListView(ListView):
    model = ObjectifParticulier
    template_name = 'pec/obj_eval_liste.html'


def json_objeval(request, pk):
    """Retourne les objectifs évaluateurs de l'obj. particulier PK"""
    objs = ObjectifEvaluateur.objects.filter(objectif_particulier=pk)
    data =[{'code': o.code, 'orient':o.orientation.nom, 'obj':o.nom, 'taxo':o.taxonomie.code} for o in objs]
    
    return HttpResponse(json.dumps(data), content_type="application/json")
    