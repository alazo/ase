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


urlpatterns = [
     url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^admin/', admin.site.urls),
    url('^tri_opar', views.TriOPar),
    url('^tri_oeva', views.TriOEva),
    url('^comp_prof_liste$', views.CompetenceProfListView.as_view(), name='competence-prof-liste'),
    url('^comp_prof/(?P<pk>\d+)$', views.CompetenceProfView.as_view(), name='competence-prof'),
    url('^comp_metho/(?P<pk>\d+)$', views.CompetenceMethoView.as_view(), name='competence-metho'),
    url('^comp_perso/(?P<pk>\d+)$', views.CompetencePersoView.as_view(), name='competence-perso'),
    url('^obj_eval$', views.ObjectifParticulierListView.as_view(), name='obj-eval-liste'),
    url('^json_objeval/(?P<pk>\d+)$', views.json_objeval),
]
