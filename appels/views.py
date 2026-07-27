from django.shortcuts import render,redirect
from .forms import EnseignantForm,MatiereForm,EtudiantForm,MotDePasseOblieForm,VerifierCodeForm,NouveauMotDePasseForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Personne,Enseignant,Matiere,Etudiant,FeuilleAppel,Presence,Inscription,Ecole
from django.db.models import Q
from django.shortcuts import get_object_or_404
import re
from urllib.parse import urlparse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
User = get_user_model()
# Create your views here.


from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def enseignant_requis(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # On vérifie si l'utilisateur a un profil enseignant
        if not request.user.is_authenticated or not hasattr(request.user, 'enseignant'):
            messages.error(request, "Accès réservé aux enseignants.")
            return redirect('connexion_enseignant')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def etudiant_requis(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # On vérifie si l'utilisateur a un profil étudiant
        if not request.user.is_authenticated or not hasattr(request.user, 'etudiant'):
            messages.error(request, "Accès réservé aux étudiants.")
            return redirect('connexion_etudiant')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
#ces fonctions servent a remplacer @login_required par @etudiant_requis et @enseignant_requis mais j'ai la fleme je vais le faire apres


def accueil(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'enseignant'):
            return redirect('dashboard')
        elif hasattr(request.user, 'etudiant'):
            return redirect('dashboard_etudiant')
        return redirect()
    return render(request,'accueil.html')


def inscription_enseignant(request):
    if request.method == "POST":
        form =  EnseignantForm(request.POST)
        if form.is_valid():
            enseignant = form.save(commit=False)
            password = form.cleaned_data.get('password')
            enseignant.set_password(password)
            enseignant.save()
            login(request, enseignant)
            messages.success(request,"Inscription reussi !")
            return redirect('dashboard')
        else:
            messages.error(request,"Erreur lors de l'inscription")
    else:
        form = EnseignantForm()
    return render(request,'enseignant/inscription_enseignant.html',{'form':form})
#http://127.0.0.1:8000/inscription-enseignant/

def connexion_enseignant(request):
    if request.method == "POST":
        identifiant = request.POST.get('username')
        p_word = request.POST.get('password')
        try:
            u_name=Personne.objects.get(Q(username=identifiant) | Q(email=identifiant))
            if u_name.check_password(p_word):
                user = u_name
            else:
                user=None
        except Personne.DoesNotExist:
            user=None

        if user is not None:
            if hasattr(user,'enseignant'):

                login(request, user)
                return redirect ('dashboard')
            else:
                messages.error(request,"Accès refusé : vous n'êtes pas autorisés")
        else:
            messages.error(request,"Identifiant ou mot de passe incorrect.")
    return render(request,'enseignant/connexion.html')
#http://127.0.0.1:8000/connexion-enseignant/


def mot_de_passe_oublier(request):
    if request.method == 'POST':
        form = MotDePasseOblieForm(request.POST)
        if form.is_valid():
            email_saisie = form.cleaned_data['email']
            user_exists = Enseignant.objects.filter(email=email_saisie).exists()
            if user_exists:
                code_recuperation = str (random.randint(100000,999999))  
                request.session['reset_email']=email_saisie
                request.session['reset_code']=code_recuperation
                delais =600
                request.session.set_expiry(delais)
                sujet= "Code de Recuperation de mot de passe"
                message = f"Bonjour,\n\nVoici votre code de récupération pour réinitialiser votre mot de passe : {code_recuperation}\n\nCe code est valide pendant 10 minutes."
                expediteur = settings.DEFAULT_FROM_EMAIL
                print("voici le code d recupération : ",code_recuperation)
                try:
                    send_mail(sujet,message,expediteur,[email_saisie])
                    messages.success(request,"Un code de verification a été envoyé a votre email")
                    return redirect('verifier_code_recuperation')
                except Exception as e:
                    messages.error(request,"Une erreur est survenue lors de l'envoie. Réessayez")
                    print("probleme",e)
            else:
                messages.error(request,"Cet utilisateur n'existe pas ou n'est pas un enseignant verifier l'email")
        else:
            print("Erreurs du formulaire :",form.errors)
    else:
        form = MotDePasseOblieForm()
    return render(request,'enseignant/mot_de_passe_oublier.html',{
        'form':form
    })

User = get_user_model()

def verifier_code_recuperation(request):
    email_saisie = request.session.get('reset_email')
    code_attendu = request.session.get('reset_code')

    if not email_saisie or not code_attendu:
        messages.error(request,"Session expirée ou invalide. Veullez recommencer")
        return redirect('mot_de_passe_oublier')
    
    code_deja_valide = request.session.get('code_verified',False)
    #code_deja_valide = False
    if not code_deja_valide:
        
        if request.method == 'POST':
            form_code = VerifierCodeForm(request.POST)
            if form_code.is_valid():
                code_saisie = form_code.cleaned_data['code_saisi']

                if code_saisie == code_attendu:
                    request.session['code_verified']=True
                    messages.success(request,"code validé avec succes")
                    return redirect('verifier_code_recuperation')
                else:
                    messages.error(request,"Code incorrect.Veuillez réesayer")
        else:
            form_code = VerifierCodeForm()

        return render(request,'enseignant/verifier_code_recuperation.html',{
        'form_code':form_code,
        'etape':'saisie_code'
        })
    else:
        if request.method=='POST':
            form_password = NouveauMotDePasseForm(request.POST)
            if form_password.is_valid():
                nouveau_password = form_password.cleaned_data['password']

                try:
                    user = Enseignant.objects.get(email=email_saisie)
                    user.set_password(nouveau_password)
                    user.save()
                    request.session.flush()
                    messages.success(request,"Mot de passe réinitialisé avec succès ! vous pouvez vous connectez")
                    return redirect('connexion_enseignant')
                except User.DoesNotExist:
                    messages.error(request,"Utilisateur introuvable")
                    return redirect('mot_de_passe_oublier')
        else:
            form_password = NouveauMotDePasseForm()
        return render(request, 'enseignant/verifier_code_recuperation.html', {
        'form_password':form_password,
        'etape': 'nouveau_password'
    })
    

@login_required
def dashboard(request):
    prof = Enseignant.objects.get(id=request.user.id)
    mes_matieres = prof.matieres.all()
    return render(request, 'enseignant/dashboard.html',{
        'prof':prof,
        'matieres':mes_matieres})
#http://127.0.0.1:8000/dashboard/

@login_required
def creer_matiere(request):
    try:
        prof = Enseignant.objects.get(id=request.user.id)
    except Enseignant.DoesNotExist:
        messages.error(request,"Seul les enseignant ont accèes à cette page")
        return redirect('connexion_enseignant')
    if request.method == 'POST':
        form = MatiereForm(request.POST)
        if form.is_valid():
            matiere = form.save(commit=False)
            matiere.enseignant = prof
            matiere.est_pondere = 'est_pondere' in request.POST
            matiere.points_presence = float(request.POST.get('points_presence', 0.0))
            matiere.points_absence = float(request.POST.get('points_absence', 0.0))
            matiere.save()
            messages.success(request,f"La matière {matiere.nom} a été créée")
            return redirect('dashboard')
    else:
        form = MatiereForm()
    mes_matieres = Matiere.objects.filter(enseignant = prof)
    toutes_les_ecoles = Ecole.objects.all().order_by('nom')
    return render(request, 'enseignant/creer_matiere.html',{
        'form':form,
        'matieres':mes_matieres,
        'ecoles_all':toutes_les_ecoles
    })
#http://127.0.0.1:8000/creer-matiere/

@login_required
def modifier_matiere(request,pk):
    matiere = get_object_or_404(Matiere,id=pk,enseignant__id=request.user.id)
    if request.method == 'POST':
        form = MatiereForm(request.POST,instance=matiere)
        if form.is_valid():
            form.save()
            messages.success(request,f"La matiere {matiere.nom} a été mise à jour")
            return redirect('dashboard')
    else:
        form = MatiereForm(instance=matiere)
    return render(request,'enseignant/modifier_matiere.html',{
        'form':form,
        'matiere': matiere
    })
@login_required
def supprimer_matiere(request,pk):
    matiere = get_object_or_404(Matiere, id=pk,enseignant__id =request.user.id)
    if request.method =='POST':
        matiere.delete()
        messages.success(request,"Matiere suppriméé definitivement.")
        return redirect(dashboard)
    return render(request,'enseignant/supprimer_matiere.html',{
        'matiere':matiere
    })

from django.db import transaction

@login_required
def reinitialiser_matiere(request, matiere_id):
    matiere = get_object_or_404(Matiere, id=matiere_id, enseignant=request.user)
    if request.method == "POST":
        with transaction.atomic():
            Presence.objects.filter(feuille__matiere=matiere).delete()
            matiere.feuilles_appel.all().delete()
            matiere.inscriptions.all().delete()
        messages.success(request, f"La matière {matiere.nom} a été réinitialisée : historique et étudiants effacés.")
        return redirect('consulter_matiere',matiere_id) 
    
    return redirect('consulter_matiere',matiere_id)

@login_required
def consulter_matiere(request,matiere_id):
    matiere = get_object_or_404(Matiere, id=matiere_id,enseignant__id=request.user.id)
    """liste_eleve = matiere.etudiants.all()
    return render(request,'enseignant/consulter_matiere.html',{
        'matiere':matiere,
        'eleves':liste_eleve
    })"""
    inscriptions = Inscription.objects.filter(matiere=matiere).select_related('etudiant')
    historique=FeuilleAppel.objects.filter(matiere=matiere).order_by('-id')
    nb_seances = FeuilleAppel.objects.filter(matiere=matiere).count()
    if matiere.est_pondere:
        for ins in inscriptions:
            ins.note_actuelle = calculer_note_assiduite(ins.etudiant, matiere)
    else:
        for ins in inscriptions:
            ins.note_actuelle = None

    nb_seances = FeuilleAppel.objects.filter(matiere=matiere).count()

    return render(request, 'enseignant/consulter_matiere.html', {
        'matiere': matiere,
        'inscriptions': inscriptions,
        'nb_seances':nb_seances,
        'historique':historique
    })

@login_required
def chercher_etudiant(request, matiere_id):
    matiere = get_object_or_404(Matiere,id=matiere_id,enseignant__id=request.user.id)
    query = request.GET.get('matricule')
    resultat =None
    erreur = None
    deja_inscrit =False
    if query:
        try:
            resultat=Etudiant.objects.get(username=query)
            if matiere.etudiants.filter(id=resultat.id).exists():
                deja_inscrit=True
        except Etudiant.DoesNotExist:
            erreur = "Aucun étudiant trouver avec ce matricule"
    return render(request,'enseignant/chercher_etudiant.html',{
        'matiere':matiere,
        'resultat':resultat,
        'erreur':erreur,
        'query':query,
        'deja_inscrit':deja_inscrit
    })

from reportlab.lib.pagesizes import A4, landscape # On utilise le mode paysage pour plus de place
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.units import cm
@login_required
def exporter_bilan_matiere_pdf(request, matiere_id):
    matiere = get_object_or_404(Matiere, id=matiere_id, enseignant=request.user)
    inscriptions = Inscription.objects.filter(matiere=matiere).select_related('etudiant')
    nb_seances = FeuilleAppel.objects.filter(matiere=matiere).count()
    from datetime import datetime
    date_str = datetime.now().strftime("%d_%m_%Y")
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Bilan_de_presences_{matiere.nom}_{matiere.ecole}_{date_str}.pdf"'

    # Configuration du document en mode Paysage (Landscape) pour faire tenir toutes les colonnes
    doc = SimpleDocTemplate(response, pagesize=A4,leftMargin=1.5*cm, rightMargin=1.5*cm)
    elements = []
    styles = getSampleStyleSheet()

    # Titre
    elements.append(Paragraph(f"Bilan d'assiduité : {matiere.nom} ({matiere.code}) : {matiere.ecole}", styles['Title']))
    elements.append(Paragraph(f"Total des séances : {nb_seances}", styles['Normal']))
    elements.append(Paragraph("<br/><br/>", styles['Normal']))

    # Données du tableau
    data = [['Matricule', 'Nom', 'Prénom', 'Présences', 'Absences', 'Points']]
    
    for ins in inscriptions:
        # On recalcule la note pour être sûr qu'elle est à jour
        note = calculer_note_assiduite(ins.etudiant, matiere)
        data.append([
            ins.etudiant.username, # ou matricule selon ton modèle
            ins.etudiant.last_name,
            ins.etudiant.first_name,
            ins.nb_presences,
            ins.nb_abscences,
            f"{note} pts" if note is not None else "N/A"
        ])

    # Style du tableau
    #t = Table(data, colWidths=[80, 150, 150, 80, 80, 80])
    t = Table(data, colWidths=[2.5*cm, 4*cm, 4*cm, 2.5*cm, 2.5*cm, 2.5*cm])
    t.hAlign = 'CENTER'
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.cadetblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    # Coloration des points négatifs en rouge
    for i, row in enumerate(data[1:], 1):
        try:
            val_note = float(row[5].replace(' pts', ''))
            if val_note < 0:
                t.setStyle(TableStyle([('TEXTCOLOR', (5, i), (5, i), colors.red)]))
            elif val_note > 0:
                t.setStyle(TableStyle([('TEXTCOLOR', (5, i), (5, i), colors.green)]))
        except:
            pass

    elements.append(t)
    doc.build(elements)
    return response

@login_required
def inscrire_etudiant_par_ensei(request,matiere_id,etudiant_id):
    matiere = get_object_or_404(Matiere,id=matiere_id,enseignant__id=request.user.id)
    etudiant = get_object_or_404(Etudiant,id=etudiant_id)
    nb_seances = FeuilleAppel.objects.filter(matiere=matiere).count()
    inscription, created =Inscription.objects.get_or_create(
        etudiant=etudiant,
        matiere=matiere,
        defaults={'nb_presences':0,'nb_abscences':nb_seances}
    )
    if created:
        messages.success(request,f"{etudiant.first_name} est maintenant inscrit à {matiere.nom}")
    else:
        messages.info(request,f"{etudiant.first_name} etait déja inscrit")
    return redirect('chercher_etudiant',matiere_id)

from django.db.models import Count, Q

def calculer_note_assiduite(etudiant, matiere):
    if not matiere.est_pondere:
        return None
    
    # On compte le nombre de présences et d'absences de l'étudiant pour CETTE matière
    stats = Presence.objects.filter(etudiant=etudiant, feuille__matiere=matiere).aggregate(
        nb_p=Count('id', filter=Q(est_present=True)),
        nb_a=Count('id', filter=Q(est_present=False))
    )
    
    # Calcul : (Presences * Pts_P) + (Absences * Pts_A)
    total = (stats['nb_p'] * matiere.points_presence) + (stats['nb_a'] * matiere.points_absence)
    return total

from django.db.models import Count
def detecter_triche(feuille_id):
    doublons =  Presence.objects.filter(feuille_id=feuille_id)\
                        .exclude(device_id__in=[None, '', 'Inconnu'])\
                        .values('device_id')\
                        .annotate(nb_utilisations=Count('device_id'))\
                        .filter(nb_utilisations__gt=1)\
                        .values_list('device_id',flat=True)
    return doublons

@login_required
def creer_feuille(request,matiere_id):
    matiere = get_object_or_404(Matiere,id=matiere_id,enseignant__id=request.user.id)
    feuille = FeuilleAppel.objects.create(matiere=matiere, date=timezone.now().date())
    return redirect('faire_appel', feuille_id=feuille.id)

from datetime import date
from django.utils import timezone
import random
@login_required
def faire_appel(request, feuille_id):
    feuille = get_object_or_404(FeuilleAppel,id=feuille_id,matiere__enseignant__id=request.user.id)
    presences = feuille.presences.all().select_related('etudiant')
    doublons_ids = detecter_triche(feuille_id)
    etudiants_suspects = Presence.objects.filter(
        feuille_id=feuille_id, 
        device_id__in=doublons_ids
    ).values_list('etudiant_id', flat=True)
    print("id des doublons",list(doublons_ids))
    matiere = feuille.matiere
    inscriptions = Inscription.objects.filter(matiere=matiere).select_related('etudiant')
    print("la matiere est ponderée",matiere.est_pondere)
    if matiere.est_pondere:
        for ins in inscriptions:
            ins.note_actuelle =calculer_note_assiduite(ins.etudiant, matiere)
    else:
        for ins in inscriptions:
            ins.note_actuelle = None
    historique=FeuilleAppel.objects.filter(matiere=matiere).order_by('-id')
    nb_seances = FeuilleAppel.objects.filter(matiere=matiere).count()
    if feuille.is_actif and feuille.date_fin_appel and timezone.now() > feuille.date_fin_appel:
        feuille.is_actif = False
        feuille.save()
        messages.warning(request, "Le temps est écoulé, l'appel a été clôturé automatiquement.")
    return render(request, 'enseignant/faire_appel.html', {
        'matiere': matiere,
        'inscriptions': inscriptions,
        'feuille': feuille,
        'nb_seances':nb_seances,
        'historique':historique,
        'presences': presences,
        'liste_tricheurs': list(doublons_ids),
        'liste_tricheurs_ids': list(etudiants_suspects)
    })

from django.utils import timezone
from datetime import timedelta
@login_required
def lancer_appel(request,feuille_id):
    feuille = get_object_or_404(FeuilleAppel,id=feuille_id,matiere__enseignant=request.user)
    if feuille.code_validation and not request.user.is_superuser:
        messages.error(request, "Cet appel a déjà été généré.")
        return redirect('faire_appel', feuille_id=feuille.id)
    duree_minutes = int(request.POST.get('duree', 5))
    rayon = int(request.POST.get('rayon', 100))
    lat = request.POST.get('lat_prof')
    lon = request.POST.get('lon_prof')
    if lat and lon and lat != "" and lon != "":
        try:
            feuille.latitude_prof = float(lat)
            feuille.longitude_prof = float(lon)
            #print("coordonées",feuille.latitude_prof,"  ",feuille.longitude_prof)
        except ValueError:
            #print ("erreur lors des coordonées")
            pass
    feuille.rayon_autorise = rayon
    code = str(random.randint(100000,999999))
    feuille.code_validation = code
    feuille.appel_lance=True
    feuille.is_actif = True
    feuille.date_fin_appel = timezone.now() + timedelta(minutes=duree_minutes)
    feuille.save()
    etudiants_inscrits = Inscription.objects.filter(matiere=feuille.matiere)
    for ins in etudiants_inscrits:
        Presence.objects.get_or_create(
            feuille=feuille,
            etudiant=ins.etudiant,
            defaults={'est_present': False}
        )
    messages.success(request, f"Appel lancé ! Le code est : {code}")
    return redirect('faire_appel', feuille_id=feuille.id)

@login_required
def cloturer_appel(request, feuille_id):
    feuille = get_object_or_404(FeuilleAppel, id=feuille_id, matiere__enseignant=request.user)
    feuille.is_actif = False
    feuille.save()
    presences_absentes = Presence.objects.filter(feuille=feuille, est_present=False)
    for p in presences_absentes:
        ins = Inscription.objects.get(etudiant=p.etudiant, matiere=feuille.matiere)
        ins.nb_abscences += 1
        ins.save()
    messages.success(request, "L'appel est maintenant clôturé et les absences ont été comptabilisées.")
    return redirect('faire_appel', feuille_id=feuille.id)

@login_required
def marquer_presence(request,feuille_id,etudiant_id,statut):
    feuille = get_object_or_404(FeuilleAppel,id=feuille_id,matiere__enseignant__id=request.user.id)
    etudiant = get_object_or_404(Etudiant,id=etudiant_id)
    inscription = get_object_or_404(Inscription,etudiant=etudiant,matiere=feuille.matiere)
    if statut=='present':
        inscription.nb_presences += 1
        stat = True
        Presence.objects.update_or_create(
            feuille=feuille,
            etudiant=etudiant,
            defaults={'est_present': stat}
        )
    elif statut=='abscent':
        inscription.nb_abscences += 1
        stat = False
        Presence.objects.update_or_create(
            feuille=feuille,
            etudiant=etudiant,
            defaults={'est_present': stat}
        ) 
    elif statut=='annulerP'and inscription.nb_presences>0:
        inscription.nb_presences -= 1
        Presence.objects.filter(feuille=feuille,etudiant=etudiant).delete()
    elif statut=='annulerA'and inscription.nb_abscences>0:
        inscription.nb_abscences -= 1
        Presence.objects.filter(feuille=feuille,etudiant=etudiant).delete()
    inscription.save()
    return redirect ('faire_appel',feuille_id=feuille.id)

@login_required
def consulter_feuille(request,feuille_id):
    feuille = get_object_or_404(FeuilleAppel,id=feuille_id,matiere__enseignant__id=request.user.id)
    pointage = Presence.objects.filter(feuille=feuille).select_related('etudiant')
    
    return render(request,'enseignant/consulter_feuille.html',{
        'feuille':feuille,
        'pointages':pointage,
        'matiere':feuille.matiere
    })

@login_required
def supprimer_feuille(request,feuille_id):
    feuille = get_object_or_404(FeuilleAppel,id=feuille_id,matiere__enseignant__id=request.user.id)
    pointages = Presence.objects.filter(feuille=feuille)
    for p in pointages:
        inscription = Inscription.objects.filter(etudiant=p.etudiant, matiere=feuille.matiere).first()
        if inscription:
            if p.est_present:
                inscription.nb_presences = max(0, inscription.nb_presences - 1)
            else:
                inscription.nb_abscences = max(0, inscription.nb_abscences - 1)
            inscription.save()
    date_feuille = feuille.date
    feuille.delete()
    messages.success(request, f"La séance du {date_feuille} a été supprimée et les compteurs ont été mis à jour.")
    return redirect('consulter_matiere',matiere_id=feuille.matiere.id)

@login_required
def vider_historique_matiere(request, matiere_id):
    matiere = get_object_or_404(Matiere, id=matiere_id, enseignant=request.user)
    if request.method == "POST":
        feuilles = FeuilleAppel.objects.filter(matiere=matiere)
        nb_seances = feuilles.count()
        with transaction.atomic():
            feuilles.delete()
            Inscription.objects.filter(matiere=matiere).update(nb_presences=0, nb_abscences=0)
        messages.success(request, f"L'historique a été vidé ({nb_seances} séances supprimées). Les statistiques des étudiants sont réinitialisées.")
        return redirect('consulter_matiere',matiere_id)
    return redirect('consulter_matiere',matiere_id)

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

@login_required
def exporter_presence_pdf(request, feuille_id):
    feuille = get_object_or_404(FeuilleAppel, id=feuille_id, matiere__enseignant=request.user)
    filtre = request.GET.get('filtre', 'tous')
    
    # Filtrage des données
    pointages = Presence.objects.filter(feuille=feuille).select_related('etudiant')
    if filtre == 'present':
        pointages = pointages.filter(est_present=True)
    elif filtre == 'absent':
        pointages = pointages.filter(est_present=False)

    # Préparation de la réponse PDF
    response = HttpResponse(content_type='application/pdf')
    filename = f"Appel_{feuille.matiere.nom}_{filtre}_{feuille.matiere.ecole}_du {feuille.date}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Création du document
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Titre et Infos
    elements.append(Paragraph(f"Feuille d'appel : {feuille.matiere.nom}: {feuille.matiere.ecole}", styles['Title']))
    elements.append(Paragraph(f"Date : {feuille.date.strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    elements.append(Paragraph(f"Filtre appliqué : {filtre.capitalize()}", styles['Normal']))
    elements.append(Paragraph("<br/><br/>", styles['Normal']))

    # Données du tableau
    data = [['Matricule', 'Nom & Prénom', 'Statut']]
    for p in pointages:
        statut = "PRESENT" if p.est_present else "ABSENT"
        data.append([
            p.etudiant.username, 
            f"{p.etudiant.last_name} {p.etudiant.first_name}", 
            statut
        ])

    # Style du tableau
    # 1. Création du tableau avec les données
    t = Table(data, colWidths=[100, 300, 80])

    # 2. Définition du style de base (En-tête, bordures, alignement)
    style_base = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]

    # 3. Ajout dynamique des couleurs (Vert pour présent, Rouge pour absent)
    for i, p in enumerate(pointages, 1):
        couleur = colors.green if p.est_present else colors.red
        style_base.append(('TEXTCOLOR', (2, i), (2, i), couleur))

    # 4. Application du style final
    t.setStyle(TableStyle(style_base))

    elements.append(t)
    doc.build(elements)
    return response

def deconnexion_enseignant(request):
    logout(request)
    return redirect('connexion_enseignant')










def inscription_etudiant(request):
    if request.method == "POST":
        form = EtudiantForm(request.POST)
        if form.is_valid():
            etudiant = form.save()
            login(request, etudiant)
            messages.success(request,'Compte étudiant créé!')
            return redirect('dashboard_etudiant')
    else:
        form = EtudiantForm()

    toutes_les_ecoles = Ecole.objects.all().order_by('nom')
    return render(request,'etudiant/inscription_etudiant.html',{'form':form,'ecoles_all':toutes_les_ecoles})
#http://127.0.0.1:8000/inscription-etudiant/

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
                messages.error(request,"Accès refusé : vous n'êtes pas autorisés")
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
        messages.error(request, "Accès refusé : tu n'as pas de profil étudiant.")
        return redirect('accueil')
    if matiere.ecole!=request.user.etudiant.ecole:
        messages.error(request, "Accès refusé : vous ne faites pas partie de cette ecole.")
        return redirect('dashboard_etudiant')
    inscription,created = Inscription.objects.get_or_create(
        etudiant=mon_profil,
        matiere=matiere,
        defaults={'nb_presences':0,'nb_abscences':nb_seances}
    )
    if created:
        messages.success(request,f"Felicitations : tu es maintenant inscrire au cour de {matiere.nom}")
    else:
        messages.info(request,f"Tu es déja inscrit au cour de {matiere.nom}")
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
                messages.error(request, "Format du lien invalide ou non autorisé.")               
        except Exception:
            messages.error(request, "Impossible d'analyser le lien fourni.")
            
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
        if timezone.now() > feuille.date_fin_appel:
            messages.error(request, "Désolé l'appel est terminé veuillez consulter votre enseignant.")
            return redirect('dashboard_etudiant')
        if (feuille.latitude_prof and feuille.longitude_prof) and feuille.rayon_autorise!=0:
            if not lat_etudiant or not lon_etudiant:
                messages.error(request, "Localisation GPS requise pour valider.")
                return redirect('dashboard_etudiant')
            distance = calculer_distance(
                feuille.latitude_prof, feuille.longitude_prof,
                float(lat_etudiant), float(lon_etudiant)
            )
            print(f"DEBUG PROF: {feuille.latitude_prof}, {feuille.longitude_prof}")
            print(f"DEBUG ETUDIANT: {lat_etudiant}, {lon_etudiant}")
            if distance > feuille.rayon_autorise:
                messages.error(request, f"Tu es trop loin de l'enseignant ({int(distance)}m). Signaler à l'enseignant en cas d'erreur")
                return redirect('dashboard_etudiant')
        if feuille.code_validation == code_saisi and feuille.is_actif:
            presence = Presence.objects.filter(feuille=feuille,etudiant=request.user.etudiant).first()
            presence.device_id=user_agent
            #print("l'identification de la machine",presence.device_id)
            if presence and not presence.est_present:
                presence.est_present = True
                presence.device_id=user_agent
                presence.save()
                inscription = Inscription.objects.get(etudiant=request.user.etudiant,matiere=feuille.matiere)
                inscription.nb_presences +=1
                inscription.save()
                messages.error(request,"Presence validéé avec succès !")
            else:
                messages.info(request,"Tu es déjà marqué(e) present")
        else:
            messages.error(request,"code incorrect ou session expirée.")
    return redirect('dashboard_etudiant')


"""ok c'est bon on a deja fait une tres bonne partie de la plateforme (le principale meme) on va maintenant faire l'annexe (stp a chaque fois que tu m'envois les template ne met plus les style sophistiqué c'est pour ne pas m'mbrouller quand je vaire faire les fichier static comme css)"""
def deconnexion_etudiant(request):
    logout(request)
    return redirect('connexion_etudiant')



# myglobalenv (c'est l'environneent virtuel)
#mot de passe du super user Clautel123456