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
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from pec import views

urlpatterns = [
    path('', views.HomeViewFE.as_view(), name='home'),
    path('admin/', admin.site.urls),

    path('index_fe/', views.HomeViewFE.as_view(), name='index-fe'),
    path('index_mp/', views.HomeViewMP.as_view(), name='index-mp'),
    path('comp_prof_liste/', views.CompetenceProfListView.as_view(), name='competence-prof-liste'),
    path('comp_prof/<int:pk>/', views.CompetenceProfView.as_view(), name='competence-prof'),
    path('comp_metho/<int:pk>/', views.CompetenceMethoView.as_view(), name='competence-metho'),
    path('comp_perso/<int:pk>/', views.CompetencePersoView.as_view(), name='competence-perso'),
    path('cours/<int:pk>/', views.CoursDetailView.as_view(), name='cours'),
    path('cours_admin/<int:pk>/', views.CoursAdminView.as_view(), name='cours-admin'),
    path('periode_fe/', views.PeriodeView.as_view(), {'filiere': 'FE'}, name='periode-fe'),
    path('periode_mp/', views.PeriodeView.as_view(), {'filiere': 'MP'}, name='periode-mp'),
    path('periode_domaine_fe/', views.PeriodeDomaineView.as_view(), {'filiere': 'FE'}, name='periode-domaine-fe'),
    path('periode_domaine_mp/', views.PeriodeDomaineView.as_view(), {'filiere': 'MP'}, name='periode-domaine-mp'),
    path('seminaire/', views.SeminaireView.as_view(), name='seminaire'),
    path('cours/', views.CoursFEListView.as_view(), name='cours'),
    path('obj_eval/', views.ObjectifParticulierListView.as_view(), name='obj-eval-liste'),
    path('json_objeval/<int:pk>/', views.json_objeval),
    path('plan_pdf_fe/', views.plan_form_pdf, {'filiere': 'FE'}, name='plan-pdf-fe'),
    path('plan_pdf_mp/', views.plan_form_pdf, {'filiere': 'MP'}, name='plan-pdf-mp'),
    path('documents/', views.DocumentListView.as_view(), name='documents'),
    path('document/<int:pk>/', views.DocumentDetailView.as_view(), name='document-detail'),
    
    # url(r'^json_objeval/(?P<pk>\d+)$', views.json_objeval),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
