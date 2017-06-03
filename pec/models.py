from django.db import models

# Create your models here.
CHOIX_ORIENTATION = (
    ('Global', 'Global'),
    ('Gén.', 'Gén.'),
    ('Enf.', 'Enf.'),
    ('PersA', 'PersA'),
    ('Hand.', 'Hand.'))



class Orientation(models.Model):
    nom = models.CharField(max_length=10, default="Global", choices = CHOIX_ORIENTATION)
    
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
    descr = models.TextField(default='', blank=True, verbose_name='description')
    abrev = models.CharField(max_length=10, blank=True, verbose_name='abréviation')
    couleur = models.CharField(max_length=10, default='', blank=True)
    
    class Meta:
        ordering = ('code',)
        
    def __str__(self):
        return '{0} -{1}'.format(self.code, self.nom)
    
    def cours_annee_1(self):
        return self.cours_set.filter(cursus=1)
    
    def cours_annee_2(self):
        return self.cours_set.filter(cursus=2)
    
    def cours_annee_3(self):
        return self.cours_set.filter(cursus=3)
        
        
class TypeCompetence(models.Model):
    nom = models.CharField(max_length=80)
    
    def __str__(self):
        return self.nom
    
       
        
class Competence(models.Model):
    PROF = 'professionnelles'
    METHODO = 'méthodologiques'
    PERSO = 'sociales et personnelles'
    
    CHOIX_TYPE_COMPETENCE = (
        (PROF, 'professionnlles.'),
        (METHODO, 'méthodologiques'),
        (PERSO, 'sociales et personnelles'))

    code = models.CharField(max_length=8, blank=False)
    nom = models.CharField(max_length=150, blank=True )
    descr = models.TextField(default='', blank=True, verbose_name='description') 
    domaine = models.ForeignKey(Domaine, null=True, on_delete = models.SET_NULL)
    
    class Meta:
        ordering = ('code',)
        verbose_name = 'Compétence'

    def __str__(self):
        return '{0} -{1}'.format(self.code, self.nom)

class CompetenceTransversale(models.Model):
    nom = models.CharField(max_length=150)
    type = models.ForeignKey(TypeCompetence, default=None, blank=False, null=True)
    
    class Meta:
        verbose_name = 'Comp. transversale'
        ordering = ('id',)
        
    def __str__(self):
        return self.nom    
    
    
    
class ObjectifParticulier(models.Model):
    tri = models.IntegerField(default=0)
    code = models.CharField(max_length=8, blank=False)
    nom = models.CharField(max_length=250, blank=True )
    competence = models.ForeignKey(Competence, default=None, null=True, on_delete = models.SET_NULL)
    competences_transversales = models.ManyToManyField(CompetenceTransversale, blank=True)
    
    class Meta:
        ordering = ('tri',)
        verbose_name = 'Obj. particulier'
        verbose_name_plural = 'Obj. particuliers'
        
    def __str__(self):
        return '{0} -{1}'.format(self.code, self.nom)
    
    
class ObjectifEvaluateur(models.Model):
    tri = models.IntegerField(default=0)
    code = models.CharField(max_length=8, blank=False)
    nom = models.TextField(default='', blank=True )
    objectif_particulier = models.ForeignKey(ObjectifParticulier, null=True, on_delete = models.SET_NULL)
    taxonomie = models.ForeignKey(Taxonomie, null=True, on_delete = models.SET_NULL)
    orientation = models.ForeignKey(Orientation, null=True, on_delete = models.SET_NULL)
    
    class Meta:
        unique_together = ('id', 'orientation')
        ordering = ('tri', 'orientation__id')
        verbose_name = 'Obj. évaluateur'
        verbose_name_plural = 'Obj. évaluateurs'
    
    def __str__(self):
        return '{0} -{1}'.format(self.code, self.nom)    
        
        
class Cursus(models.Model):
    code = models.CharField(max_length=10, blank=False, unique=True)
     
    def __str__(self):
        return self.code

    class Meta:
        ordering = ('code', )
        verbose_name_plural = 'Cursus'

    
class Cours(models.Model):
    nom = models.CharField(max_length=40, blank=False)
    descr = models.TextField(blank=True, verbose_name='description')
    objectifs_evaluateurs = models.ManyToManyField(ObjectifEvaluateur,blank=True)
    cursus = models.ForeignKey(Cursus, null=True, on_delete = models.SET_NULL)
    type = models.CharField(max_length=30, blank=True)
    periode = models.IntegerField()
    nbre_note = models.IntegerField()
    domaine = models.ForeignKey(Domaine, default=None,  null=True, on_delete = models.SET_NULL)
    careum = models.CharField(max_length=10, default='')
    
    class Meta:
        unique_together = ('cursus', 'nom')
        ordering = ('nom',)
        verbose_name_plural = 'Cours'
         
    def __str__(self):
        return '{0} - {1}'.format(self.cursus.code, self.nom)
     
    
     
     
            