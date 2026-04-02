from django.contrib import admin
from .models import Personne, Enseignant,Matiere,Etudiant,Inscription,FeuilleAppel,Presence,Ecole

# Register your models here.
admin.site.register(Personne)
admin.site.register(Enseignant)
admin.site.register(Matiere)
admin.site.register(Etudiant)
admin.site.register(Inscription)
admin.site.register(FeuilleAppel)
admin.site.register(Presence)
admin.site.register(Ecole)