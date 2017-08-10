"""ase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from pec import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.HomeViewFE.as_view(), name='home'),
    url(r'^admin/', admin.site.urls),
    
    # url(r'^tri_opar', views.TriOPar),
    # url(r'^tri_oeva', views.TriOEva),
    url(r'^index_fe$', views.HomeViewFE.as_view(), name='index-fe'),
    url(r'^index_mp$', views.HomeViewMP.as_view(), name='index-mp'),
    url(r'^comp_prof_liste$', views.CompetenceProfListView.as_view(), name='competence-prof-liste'),
    url(r'^comp_prof/(?P<pk>\d+)$', views.CompetenceProfView.as_view(), name='competence-prof'),
    url(r'^comp_metho/(?P<pk>\d+)$', views.CompetenceMethoView.as_view(), name='competence-metho'),
    url(r'^comp_perso/(?P<pk>\d+)$', views.CompetencePersoView.as_view(), name='competence-perso'),
    url(r'^cours/(?P<pk>\d+)$', views.CoursDetailView.as_view(), name='cours'),
    url(r'^cours_admin/(?P<pk>\d+)$', views.CoursAdminView.as_view(), name='cours-admin'),
    url(r'^periode_fe$', views.PeriodeView.as_view(), {'filiere': 'FE'}, name='periode-fe'),
    url(r'^periode_mp$', views.PeriodeView.as_view(), {'filiere': 'MP'}, name='periode-mp'),
    url(r'^periode_domaine_fe$', views.PeriodeDomaineView.as_view(), {'filiere': 'FE'}, name='periode-domaine-fe'),
    url(r'^periode_domaine_mp$', views.PeriodeDomaineView.as_view(), {'filiere': 'MP'}, name='periode-domaine-mp'),
    url(r'^seminaire$', views.SeminaireView.as_view(), name='seminaire'),
    url(r'^cours/$', views.CoursFEListView.as_view(), name='cours'),
    url(r'^obj_eval$', views.ObjectifParticulierListView.as_view(), name='obj-eval-liste'),
    url(r'^json_objeval/(?P<pk>\d+)$', views.json_objeval),
    url(r'^plan_pdf_fe$', views.plan_form_pdf, {'filiere': 'FE'}, name='plan-pdf-fe'),
    url(r'^plan_pdf_mp$', views.plan_form_pdf, {'filiere': 'MP'}, name='plan-pdf-mp'),
    url(r'^documents$', views.DocumentListView.as_view(), name='documents'),
    url(r'^document/(?P<pk>\d+)$', views.DocumentDetailView.as_view(), name='document-detail'),
    
    #url(r'^json_objeval/(?P<pk>\d+)$', views.json_objeval),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )
