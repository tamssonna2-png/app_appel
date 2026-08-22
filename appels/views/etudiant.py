from django.shortcuts import render,redirect
from ..forms import EnseignantForm,MatiereForm,EtudiantForm,MotDePasseOblieForm,VerifierCodeForm,NouveauMotDePasseForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import Personne,Enseignant,Matiere,Etudiant,FeuilleAppel,Presence,Inscription,Ecole
from django.db.models import Q
from django.shortcuts import get_object_or_404
import re
from urllib.parse import urlparse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _ #messages.success(request, _("Votre présence a bien été enregistrée.")) comment utiliser
User = get_user_model()

from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def etudiant_requis(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # On vérifie si l'utilisateur a un profil étudiant
        if not request.user.is_authenticated or not hasattr(request.user, 'etudiant'):
            messages.error(request, _("Accès réservé aux étudiants."))
            return redirect('connexion_etudiant')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


import random

def inscription_etudiant(request):
    if request.method == "POST":
        form = EtudiantForm(request.POST)
        if form.is_valid():
            etudiant = form.save(commit=False)
            etudiant.is_active = False
            etudiant.save()
            code_verification = str (random.randint(100000,999999))  
            request.session['signupe_email']=etudiant.email #est ce qu'on a besoin de ca
            request.session['signupe_code']=code_verification# et de ca ?
            delais =600
            request.session.set_expiry(delais)
            sujet= "Validation de votre compte etudiant sur ATTENDO"
            message = f"Bonjour {etudiant.first_name},\n\nVotre code de vérification est : {code_verification}\n\nCe code est valide pendant 10 minutes."
            expediteur = settings.DEFAULT_FROM_EMAIL
            print("voici le code d recupération : ",code_verification)
            try:
                send_mail(sujet,message,expediteur,[etudiant.email])
                messages.success(request,_("Un code de verification a été envoyé a votre email"))
                return redirect('verifier_email_etudiant')
            except Exception as e:
                if etudiant.pk:
                    etudiant.delete()
                messages.error(request,_("Une erreur est survenue lors de l'envoie. Réessayez"))
                print("probleme",e)
            """login(request, etudiant)
            messages.success(request,_('Compte étudiant créé!'))
            return redirect('dashboard_etudiant')"""
    else:
        form = EtudiantForm()

    toutes_les_ecoles = Ecole.objects.all().order_by('nom')

    return render(request,'etudiant/inscription_etudiant.html',{'form':form,'ecoles_all':toutes_les_ecoles})
#http://127.0.0.1:8000/inscription-etudiant/

def verifier_email_etudiant(request):
    email_saisie = request.session.get('signupe_email')
    code_attendu = request.session.get('signupe_code')

    # Sécurité : Si pas de session, retour à l'inscription
    if not email_saisie or not code_attendu:
        messages.error(request, _("Session expirée ou invalide. Veuillez recommencer."))
        return redirect('inscription_etudiant')
    
    if request.method == 'POST':
        form_code = VerifierCodeForm(request.POST)
        if form_code.is_valid():
            code_saisi = form_code.cleaned_data['code_saisi']

            if code_saisi == code_attendu:
                try:
                    # 1. Récupération et activation de l'utilisateur
                    etudiant = User.objects.get(email=email_saisie)
                    etudiant.is_active = True
                    etudiant.save()

                    # 2. Nettoyage des variables de session
                    del request.session['signupe_email']
                    del request.session['signupe_code']

                    # 3. Connexion automatique (ou redirection vers connexion)
                    login(request, etudiant) # Optionnel : connecte l'utilisateur directement
                    
                    messages.success(request, _("Votre compte a été activé avec succès ! Bienvenue."))
                    return redirect('dashboard_etudiant')

                except User.DoesNotExist:
                    messages.error(request, _("Utilisateur introuvable. Veuillez vous réinscrire."))
                    return redirect('inscription_etudiant')
            else:
                messages.error(request, _("Code incorrect. Veuillez réessayer."))
    else:
        form_code = VerifierCodeForm()

    return render(request, 'etudiant/verifier_email_etudiant.html', {
        'form_code': form_code,
        'etape': 'saisie_code'
    })

from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def connexion_etudiant(request):
    if request.user.is_authenticated and hasattr(request.user, 'etudiant') and request.method == "GET":
        return redirect('dashboard_etudiant')
    if request.method == "POST":
        identifiant = request.POST.get('username')
        try:
            user=Personne.objects.get(Q(username=identifiant) | Q(email=identifiant))
            #user = authenticate(request,username=u_name.username)
            if hasattr(user,'etudiant'):
                login(request, user)
                return redirect ('dashboard_etudiant')
            else:
                messages.error(request,_("Accès refusé : vous n'êtes pas autorisés"))
        except Personne.DoesNotExist:
            user=None
        #if user is not None:
            """if hasattr(user,'etudiant'):
                login(request, user)
                return redirect ('dashboard_etudiant')
            else:
                messages.error(request,"Accès refusé : vous n'êtes pas autorisés")"""
        #else:
            #messages.error(request,"Matricule ou email inconnu.")
    return render(request,'etudiant/connexion_etudiant.html')


@login_required(login_url='connexion_etudiant')
def dashboard_etudiant(request):
    mes_inscriptions=Inscription.objects.filter(etudiant=request.user.etudiant)
    etudiant=get_object_or_404(Etudiant,id=request.user.id)
    return render(request,'etudiant/dashboard_etudiant.html',{
        'inscriptions':mes_inscriptions,
        'etudiant':etudiant
        })


@login_required
def inscription_matiere(request,matiere_id):
    matiere = get_object_or_404(Matiere,id=matiere_id)
    nb_seances = FeuilleAppel.objects.filter(matiere=matiere).count()
    try:
        mon_profil = request.user.etudiant # Adapte selon ton modèle
    except AttributeError:
        messages.error(request, _("Accès refusé : tu n'as pas de profil étudiant."))
        return redirect('accueil')
    if matiere.ecole!=request.user.etudiant.ecole:
        messages.error(request, _("Accès refusé : vous ne faites pas partie de cette ecole."))
        return redirect('dashboard_etudiant')
    inscription,created = Inscription.objects.get_or_create(
        etudiant=mon_profil,
        matiere=matiere,
        defaults={'nb_presences':0,'nb_abscences':nb_seances}
    )
    if created:
         messages.success(request, _("Felicitations : tu es maintenant inscrire au cour de %(nom)s") % {'nom': matiere.nom})
    else:
        messages.info(request, _("Tu es déja inscrit au cour de %(nom)s") % {'nom': matiere.nom})
    return redirect('dashboard_etudiant')

@login_required
def traiter_lien_inscription(request):
    if request.method == 'POST':
        lien = request.POST.get('lien_complet', '').strip()       
        try:
            chemin = urlparse(lien).path
            match = re.search(r'^/student/(?:inscrire|inscription)-matiere/(\d+)/?$', chemin)           
            if match:
                matiere_id = int(match.group(1))
                return redirect('inscription_matiere', matiere_id=matiere_id)
            else:
                messages.error(request, _("Format du lien invalide ou non autorisé."))               
        except Exception:
            messages.error(request,_("Impossible d'analyser le lien fourni."))
            
    return redirect('dashboard_etudiant')


from math import radians, cos, sin, asin, sqrt

def calculer_distance(lat1, lon1, lat2, lon2):
    R = 6371000 
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

@login_required
def valider_presence(request):
    if request.method =='POST':
        user_agent = request.META.get('HTTP_USER_AGENT','Inconnu')
        feuille_id = request.POST.get('feuille_id')
        code_saisi = request.POST.get('code_saisi')
        lat_etudiant = request.POST.get('lat_etudiant')
        lon_etudiant = request.POST.get('lon_etudiant')
        feuille = get_object_or_404(FeuilleAppel,id=feuille_id)
        inscription = Inscription.objects.get(etudiant=request.user.etudiant,matiere=feuille.matiere)
        if timezone.now() > feuille.date_fin_appel:
            messages.error(request, _("Désolé l'appel est terminé veuillez consulter votre enseignant."))
            #inscription.nb_abscences +=1
            #inscription.save()
            return redirect('dashboard_etudiant')
        if (feuille.latitude_prof and feuille.longitude_prof) and feuille.rayon_autorise!=0:
            if not lat_etudiant or not lon_etudiant:
                messages.error(request, _("Localisation GPS requise pour valider."))
                return redirect('dashboard_etudiant')
            distance = calculer_distance(
                feuille.latitude_prof, feuille.longitude_prof,
                float(lat_etudiant), float(lon_etudiant)
            )
            print(f"DEBUG PROF: {feuille.latitude_prof}, {feuille.longitude_prof}")
            print(f"DEBUG ETUDIANT: {lat_etudiant}, {lon_etudiant}")
            if distance > feuille.rayon_autorise:
                messages.error(request, _("Tu es trop loin de l'enseignant (%(distance)sm). Signaler à l'enseignant en cas d'erreur") % {'distance': int(distance)})
                return redirect('dashboard_etudiant')
        if feuille.code_validation == code_saisi and feuille.is_actif:
            presence = Presence.objects.filter(feuille=feuille,etudiant=request.user.etudiant).first()
            presence.device_id=user_agent
            #print("l'identification de la machine",presence.device_id)
            if presence and not presence.est_present:
                presence.est_present = True
                presence.device_id=user_agent
                presence.save()
                #inscription = Inscription.objects.get(etudiant=request.user.etudiant,matiere=feuille.matiere)
                inscription.nb_presences +=1
                inscription.save()
                messages.success(request,_("Presence validéé avec succès !"))
            else:
                messages.info(request,_("Tu es déjà marqué(e) present"))
        else:
            messages.error(request,_("code incorrect ou session expirée."))
    return redirect('dashboard_etudiant')


"""ok c'est bon on a deja fait une tres bonne partie de la plateforme (le principale meme) on va maintenant faire l'annexe (stp a chaque fois que tu m'envois les template ne met plus les style sophistiqué c'est pour ne pas m'mbrouller quand je vaire faire les fichier static comme css)"""
def deconnexion_etudiant(request):
    logout(request)
    return redirect('connexion_etudiant')
    