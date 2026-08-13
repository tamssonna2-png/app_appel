from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Ecole(models.Model):
    nom = models.CharField(max_length=200,unique=True)
    abreviation = models.CharField(max_length=20,unique=True)
    adresse = models.CharField(max_length=255,blank=True)

    def __str__(self):
        return self.abreviation
    
class Personne (AbstractUser):
    SEXE_CHOICES = [
        ('M','Masculin'),
        ('F','Feminin'),
    ]
    email = models.EmailField(unique=True,blank=False)
    telephone = models.CharField(max_length=20,blank=True)

    sexe = models.CharField(
        max_length=1,
        choices=SEXE_CHOICES,
        verbose_name="Sexe",
        null=True,
        blank=True
    )
    class Meta:
        #db_table = ''
        #managed = True
        verbose_name = 'Utilisateur Systeme'
        verbose_name_plural = 'Utilisateurs Systeme'

    def __str__(self):
        nom = self.last_name if self.last_name else self.username
        return f"{nom}  {self.email}"
    

class Enseignant(Personne):
    specialite = models.CharField(max_length=100)
    ecole = models.ManyToManyField(Ecole,related_name="enseignant")
    class Meta:
        #db_table = ''
        #managed = True
        verbose_name = 'Enseignant'
        verbose_name_plural = 'Enseignants'

    def __str__(self):
        nom_complet = super().__str__()
        return f"{nom_complet} {self.specialite}"
    

class Matiere(models.Model):
    nom = models.CharField(max_length=20)
    code = models.CharField(max_length=15)
    credit = models.PositiveIntegerField()
    description = models.CharField(max_length=100,null=True, blank=True)
    enseignant = models.ForeignKey(Enseignant,on_delete=models.SET_NULL, related_name="matieres",null=True,blank=True) 
    ecole = models.ForeignKey(Ecole,on_delete=models.CASCADE,related_name="matieres")
    est_pondere = models.BooleanField(default=False)
    points_presence = models.FloatField(default=0.0)
    points_absence = models.FloatField(default=0.0)
    def __str__(self):
        return f"{self.nom} {self.code} {self.credit} {self.ecole.abreviation}"
    def a_un_appel_actif(self):
        return self.feuilles_appel.filter(is_actif=True).first()

class Etudiant(Personne):
    matricule = models.CharField(max_length=100,unique=True)
    matieres = models.ManyToManyField(Matiere,through='Inscription',related_name="etudiants")
    ecole = models.ForeignKey(
        Ecole,
        on_delete=models.PROTECT,
        related_name='etudiants',
        null=False,
        blank=False
    )

    class Meta:
        #db_table = ''
        #managed = True
        verbose_name = 'Etudiant'
        verbose_name_plural = 'Etudiants'

    def __str__(self):
        nom_complet = super().__str__()
        return f"{nom_complet} {self.matricule}"
    
class Inscription(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere,on_delete=models.CASCADE,related_name='inscriptions')
    nb_presences = models.PositiveBigIntegerField(default=0)
    nb_abscences = models.PositiveBigIntegerField(default=0)
    note_actuelle = models.FloatField(null=True,blank=True)
    class Meta:
        unique_together = ('etudiant','matiere')
    def __str__(self):
        return f"{self.etudiant} inscrit en {self.matiere}"
    @property
    def total_seances(self):
        return self.nb_abscences + self.nb_presences
    @property
    def taux_presence(self):
        total = self.total_seances
        if total == 0:
            return 0
        return round((self.nb_presences/total)*100,1)

class FeuilleAppel(models.Model):
    matiere = models.ForeignKey(Matiere,on_delete=models.CASCADE,related_name="feuilles_appel")
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255,blank=True,help_text="Ex, cours sur le beton armée")
    code_validation = models.CharField(max_length=6,blank=True,null=True)
    is_actif = models.BooleanField(default=False)
    appel_lance = models.BooleanField(default=False)
    date_fin_appel = models.DateTimeField(null=True,blank=True)
    rayon_autorise = models.FloatField(null=True,blank=True)
    latitude_prof = models.FloatField(null=True,blank=True)
    longitude_prof = models.FloatField(null=True,blank=True)
    def __str__(self):
        return f"Appel - {self.matiere.nom} - {self.date}"
    @property
    def secondes_restantes(self):
        if self.is_actif and self.date_fin_appel:
            from django.utils import timezone
            diff = self.date_fin_appel - timezone.now()
            return max(0, int(diff.total_seconds()))
        return 0
    
class Presence(models.Model):
    feuille = models.ForeignKey(FeuilleAppel,on_delete=models.CASCADE,related_name="presences")
    etudiant = models.ForeignKey(Etudiant,on_delete=models.CASCADE)
    est_present = models.BooleanField(default=True)
    lat = models.FloatField(null=True,blank=True)#lattitude de l'etudiant
    lon = models.FloatField(null=True,blank=True)#longitude de l'etudiant c'est pour determiner la position geographique en fonction de celui  du professeur à chaque cours
    device_id = models.CharField(max_length=255,null=True,blank=True)
    class Meta:
        unique_together = ('feuille','etudiant')

    def __str__(self):
        statut = "Present" if self.est_present else "Absant"
        return f"{self.etudiant.last_name} - {statut}"
    
