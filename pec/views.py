from django.shortcuts import render

# Create your views here.
from .models import ObjectifParticulier, ObjectifEvaluateur


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