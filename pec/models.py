import os

from django.db import models
from django.conf import settings

# Create your models here.
CHOIX_ORIENTATION = (
    ('Global', 'Global'),
    ('Gén.', 'Gén.'),
    ('Enf.', 'Enf.'),
    ('PersA', 'PersA'),
    ('Hand.', 'Hand.'))


class Orientation(models.Model):
    nom = models.CharField(max_length=10, default="Global", choices=CHOIX_ORIENTATION)
    
    def __str__(self):
        return self.nom


class Taxonomie(models.Model):
    code = models.CharField(max_length=5, blank=False)
    descr = models.TextField(default='', blank=True, verbose_name='description')

    class Meta:
        ordering = ('code',)

    def __str__(self):
        return '{0}'.format(self.code)


class Domaine(models.Model):
    code = models.CharField(max_length=8, blank=False)
    nom = models.CharField(max_length=100, blank=False, unique=True)
    descr = models.TextField('description', default='', blank=True)
    abrev = models.CharField('abréviation', max_length=10, blank=True)
    couleur = models.CharField(max_length=10, default='', blank=True)
    
    class Meta:
        ordering = ('code',)

    def __str__(self):
        return '{0} -{1}'.format(self.code, self.nom)

    def cours_fe_annee_1(self):
        return self.cours_set.filter(cursus__code='1FE').exclude(index_published=False)

    def cours_fe_annee_2(self):
        return self.cours_set.filter(cursus=2).exclude(index_published=False)

    def cours_fe_annee_3(self):
        return self.cours_set.filter(cursus=3).exclude(index_published=False)

    def cours_mp_annee_1(self):
        return self.cours_set.filter(cursus=4).exclude(index_published=False)

    def cours_mp_annee_2(self):
        return self.cours_set.filter(cursus=5).exclude(index_published=False)

    def cours_mp_annee_3(self):
        return self.cours_set.filter(cursus=6).exclude(index_published=False)    


class TypeCompetence(models.Model):
    nom = models.CharField(max_length=80)

    def __str__(self):
        return self.nom


class Competence(models.Model):
    """Compétence de base selon PEC """
    code = models.CharField(max_length=8, blank=False)
    nom = models.CharField(max_length=150, blank=True)
    descr = models.TextField(default='', blank=True, verbose_name='description') 
    domaine = models.ForeignKey(Domaine, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('code',)
        verbose_name = 'Compétence'

    def __str__(self):
        return '{0} -{1}'.format(self.code, self.nom)


class CompetenceTransversale(models.Model):
    """Compétence transversale selon PEC-ASE (méthodologiques et personnelles)"""
    nom = models.CharField(max_length=150)
    type = models.ForeignKey(TypeCompetence, default=None, blank=False, null=True, on_delete=models.SET_NULL)
    
    class Meta:
        verbose_name = 'Comp. transversale'
        ordering = ('id',)
        
    def __str__(self):
        return self.nom    
    
      
class ObjectifParticulier(models.Model):
    """Objectif particulier selon PEC-ASE (24 obj. part.)"""
    tri = models.IntegerField(default=0)
    code = models.CharField(max_length=8, blank=False)
    nom = models.CharField(max_length=250, blank=True)
    competence = models.ForeignKey(Competence, default=None, null=True, blank=True, on_delete=models.SET_NULL)
    competences_transversales = models.ManyToManyField(CompetenceTransversale, blank=True)
    
    class Meta:
        ordering = ('tri',)
        verbose_name = 'Obj. particulier'
        verbose_name_plural = 'Obj. particuliers'
        
    def __str__(self):
        return '{0} -{1}'.format(self.code, self.nom)
    
    
class ObjectifEvaluateur(models.Model):
    """Objectif éval. selon PEC-ASE (278 obj. part.)
    Ne garder que les objectifs Globaux et Gén.
    """
    tri = models.IntegerField(default=0)
    code = models.CharField(max_length=8, blank=False)
    nom = models.TextField(default='', blank=True)
    objectif_particulier = models.ForeignKey(ObjectifParticulier, null=True, default=None, blank=True, on_delete=models.SET_NULL)
    taxonomie = models.ForeignKey(Taxonomie, null=True, default=None, blank=True,  on_delete=models.SET_NULL)
    orientation = models.ForeignKey(Orientation, null=True, default=None, blank=True, on_delete=models.SET_NULL)
    
    class Meta:
        unique_together = ('id', 'orientation')
        ordering = ('tri', )
        verbose_name = 'Obj. évaluateur'
        verbose_name_plural = 'Obj. évaluateurs'
    
    def __str__(self):
        return '{0}-{1}-{2}'.format(self.code, self.orientation.nom[:3], self.nom[:20])    
        
        
class Cursus(models.Model):
    """ Regroupe l'année et dormation et la filière
        Ex: 1MP, 3FE, etc
    """
    code = models.CharField(max_length=10, blank=False, unique=True)
     
    def __str__(self):
        return self.code

    class Meta:
        ordering = ('code', )
        verbose_name_plural = 'Cursus'

    
class Cours(models.Model):
    """ Cours de la formation ASE"""
    nom = models.CharField(max_length=40, blank=False)
    descr = models.TextField(blank=True, verbose_name='description')
    objectifs_evaluateurs = models.ManyToManyField(ObjectifEvaluateur, blank=True)
    type = models.CharField(max_length=30, blank=True)
    periode = models.IntegerField()
    nbre_note = models.IntegerField()
    domaine = models.ForeignKey(Domaine, default=None,  null=True, blank=True, on_delete=models.SET_NULL)
    careum = models.CharField(max_length=30, default='')
    cursus = models.ManyToManyField(Cursus, blank=True)
    index_published = models.BooleanField(default=True)
    evaluation = models.CharField(max_length=150, blank=True)
    didactique = models.CharField(max_length=150, blank=True)
    # cursus = models.CharField(max_length=20, blank=True)
    
    class Meta:
        # unique_together = ('nom', 'periode')
        ordering = ('nom',)
        verbose_name_plural = 'Cours'
         
    def __str__(self):
        return '{0}'.format(self.nom)
     
    def formation(self):
        # foo = [x.code for x in self.cursus.all()]
        return ', '.join([x.code for x in self.cursus.all()])
    
    def get_cursus(self):
        foo = [x.code for x in self.cursus.all()]
        print(foo)
        return ', '.join(foo)

    def get_objectifs_evaluateurs(self):
        bar = []
        for sequence in self.sequence_set.all():
            for obj in sequence.objectifs_evaluateurs.all().order_by('tri'):
                bar.append(obj.id)
        bar.sort()
        return ObjectifEvaluateur.objects.filter(id__in=bar).order_by('tri')


class Sequence(models.Model):
    """Séquence pédagogique à l'intérieur d'un cours"""
    titre = models.CharField(max_length=100, blank=False)
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    periode = models.IntegerField(blank=False)
    contenu = models.TextField(blank=True)
    objectifs_evaluateurs = models.ManyToManyField(ObjectifEvaluateur, blank=True)
    objectifs_apprentissage = models.TextField(blank=True)
    careum = models.CharField(max_length=20, default='', blank=True)
    
    def __str__(self):
        return self.titre

    def get_objectifs_evaluateurs_txt(self):
        foo = [x.code for x in self.objectifs_evaluateurs.all()]
        return ', '.join(foo)


class Document(models.Model):
    """Document à uploader"""
    path = models.FileField(upload_to='doc/')
    titre = models.CharField(max_length=100, blank=False)
    published = models.BooleanField(default=False)
    
    def __str__(self):
        return self.titre    
    
    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.path.name))
        super(Document, self).delete(*args, **kwargs)
