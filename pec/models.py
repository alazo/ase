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
    
    def cours_fe_annee_1(self):
        return self.cours_set.filter(cursus=1).exclude(index_published=False)
    
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
    nom = models.CharField(max_length=150, blank=True )
    descr = models.TextField(default='', blank=True, verbose_name='description') 
    domaine = models.ForeignKey(Domaine, null=True, on_delete = models.SET_NULL)
    
    class Meta:
        ordering = ('code',)
        verbose_name = 'Compétence'

    def __str__(self):
        return '{0} -{1}'.format(self.code, self.nom)


class CompetenceTransversale(models.Model):
    """Compétence transversale selon PEC-ASE (méthodologiques et personnelles)"""
    nom = models.CharField(max_length=150)
    type = models.ForeignKey(TypeCompetence, default=None, blank=False, null=True)
    
    class Meta:
        verbose_name = 'Comp. transversale'
        ordering = ('id',)
        
    def __str__(self):
        return self.nom    
    
      
class ObjectifParticulier(models.Model):
    """Objectif particulier selon PEC-ASE (24 obj. part.)"""
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
    """Objectif éval. selon PEC-ASE (278 obj. part.)
    Ne garder que les objectifs Globaux et Gén.
    """
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
    objectifs_evaluateurs = models.ManyToManyField(ObjectifEvaluateur,blank=True)
    type = models.CharField(max_length=30, blank=True)
    periode = models.IntegerField()
    nbre_note = models.IntegerField()
    domaine = models.ForeignKey(Domaine, default=None,  null=True, on_delete = models.SET_NULL)
    careum = models.CharField(max_length=10, default='')
    cursus = models.ManyToManyField(Cursus, blank=True)
    #formation = models.CharField(max_length=10, blank=True)
    index_published = models.BooleanField(default=True)
    
    #cursus = models.CharField(max_length=20, blank=True)
    
    class Meta:
        #unique_together = ('nom', 'periode')
        ordering = ('nom',)
        verbose_name_plural = 'Cours'
         
    def __str__(self):
        return '{0} - {1}'.format(self.formation, self.nom)
     
    def cursus_txt(self):
        #foo = [x.code for x in self.cursus.all()]
        return ', '.join([x.code for x in self.cursus.all()])
     
     
            