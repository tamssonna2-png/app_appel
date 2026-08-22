from django.urls import path
from . import views

"""urlpatterns = [
    path('',views.accueil,name='accueil'),
    path('inscription-enseignant/',views.inscription_enseignant,name='inscription_enseignant'),
    path('connexion-enseignant/',views.connexion_enseignant,name='connexion_enseignant'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('deconnexion_enseignant/', views.deconnexion_enseignant,name='deconnexion_enseignant'),
    path('creer-matiere/',views.creer_matiere,name='creer_matiere'),
    path('modifier-matiere/<int:pk>/',views.modifier_matiere,name='modifier_matiere'),
    path('reinitialiser-matiere/<int:matiere_id>/',views.reinitialiser_matiere,name='reinitialiser_matiere'),
    path('supprimer-matiere/<int:pk>/',views.supprimer_matiere,name='supprimer_matiere'),
    path('consulter-matiere/<int:matiere_id>/',views.consulter_matiere,name='consulter_matiere'),
    path('exporter-bilan-pdf/<int:matiere_id>/',views.exporter_bilan_matiere_pdf,name='exporter_bilan_pdf'),
    path('creer-feuille/<int:matiere_id>/',views.creer_feuille,name='creer_feuille'),
    path('faire-appel/<int:feuille_id>/',views.faire_appel,name='faire_appel'),
    path('chercher-etudiant/<int:matiere_id>/',views.chercher_etudiant,name='chercher_etudiant'),
    path('inscrire-etudiant-par-ensei/<int:matiere_id>/<int:etudiant_id>/',views.inscrire_etudiant_par_ensei,name='inscrire_etudiant_par_ensei'),
    path('marquer-presence/<int:feuille_id>/<int:etudiant_id>/<str:statut>/',views.marquer_presence,name='marquer_presence'),
    path('lancer-appel/<int:feuille_id>/',views.lancer_appel,name='lancer_appel'),
    path('cloturer-appel/<int:feuille_id>/', views.cloturer_appel, name='cloturer_appel'),
    path('consulter-feuille/<int:feuille_id>/',views.consulter_feuille,name='consulter_feuille'),
    path('supprimer-feuille/<int:feuille_id>/',views.supprimer_feuille,name='supprimer_feuille'),
    path('vider_historique_matiere/<int:matiere_id>/',views.vider_historique_matiere,name='vider_historique_matiere'),
  
    path('exporter_pdf/<int:feuille_id>/',views.exporter_presence_pdf,name='exporter_pdf'),
    path('inscription-etudiant/',views.inscription_etudiant,name='inscription_etudiant'),
    path('connexion-etudiant/',views.connexion_etudiant,name='connexion_etudiant'),
    path('dashboard-etudiant/',views.dashboard_etudiant,name='dashboard_etudiant'),
    path('inscription-matiere/<int:matiere_id>/',views.inscription_matiere,name='inscription_matiere'),
    path('traiter-lien-inscription/',views.traiter_lien_inscription,name='traiter_lien_inscription'),
    path('valider-presence/',views.valider_presence,name='valider_presence'),
    path('deconnexion-etudiant/', views.deconnexion_etudiant, name='deconnexion_etudiant'),
]"""

urlpatterns = [
    # --- ACCUEIL GÉNÉRAL ---
    path('', views.accueil, name='accueil'),

    # ==========================================
    #   ESPACE ENSEIGNANT (LANCER / GESTION)
    # ==========================================
    # Authentification Pro
    path('pro/inscription/', views.inscription_enseignant, name='inscription_enseignant'),
    path('pro/verifier-email/',views.verifier_email,name='verifier_email'),
    path('pro/connexion/', views.connexion_enseignant, name='connexion_enseignant'),
    path('pro/deconnexion/', views.deconnexion_enseignant, name='deconnexion_enseignant'),
    path('pro/dashboard/', views.dashboard, name='dashboard'),
    path('pro/mot-de-passe-oublier',views.mot_de_passe_oublier,name='mot_de_passe_oublier'),
    path('pro/verifier-code',views.verifier_code_recuperation,name='verifier_code_recuperation'),

    # Gestion des Matières (CRUD)
    path('pro/matiere/creer/', views.creer_matiere, name='creer_matiere'),
    path('pro/matiere/modifier/<int:pk>/', views.modifier_matiere, name='modifier_matiere'),
    path('pro/matiere/consulter/<int:matiere_id>/', views.consulter_matiere, name='consulter_matiere'),
    path('pro/matiere/supprimer/<int:pk>/', views.supprimer_matiere, name='supprimer_matiere'),
    path('pro/matiere/reinitialiser/<int:matiere_id>/', views.reinitialiser_matiere, name='reinitialiser_matiere'),
    path('pro/matiere/vider-historique/<int:matiere_id>/', views.vider_historique_matiere, name='vider_historique_matiere'),

    # Gestion des Étudiants par l'Enseignant
    path('pro/matiere/<int:matiere_id>/chercher-etudiant/', views.chercher_etudiant, name='chercher_etudiant'),
    path('pro/matiere/<int:matiere_id>/inscrire-etudiant/<int:etudiant_id>/', views.inscrire_etudiant_par_ensei, name='inscrire_etudiant_par_ensei'),

    # Gestion de l'Appel (Feuilles)
    path('pro/appel/creer/<int:matiere_id>/', views.creer_feuille, name='creer_feuille'),
    path('pro/appel/faire/<int:feuille_id>/', views.faire_appel, name='faire_appel'),
    path('pro/appel/lancer/<int:feuille_id>/', views.lancer_appel, name='lancer_appel'),
    path('pro/appel/cloturer/<int:feuille_id>/', views.cloturer_appel, name='cloturer_appel'),
    path('pro/appel/consulter/<int:feuille_id>/', views.consulter_feuille, name='consulter_feuille'),
    path('pro/appel/supprimer/<int:feuille_id>/', views.supprimer_feuille, name='supprimer_feuille'),
    path('pro/appel/marquer/<int:feuille_id>/<int:etudiant_id>/<str:statut>/', views.marquer_presence, name='marquer_presence'),

    # Exports PDF Pro
    path('pro/export/feuille-pdf/<int:feuille_id>/', views.exporter_presence_pdf, name='exporter_pdf'),
    path('pro/export/bilan-pdf/<int:matiere_id>/', views.exporter_bilan_matiere_pdf, name='exporter_bilan_pdf'),


    # ==========================================
    #   ESPACE ÉTUDIANT (POINTAGE / INSCRIPTION)
    # ==========================================
    # Authentification Étudiant
    path('student/inscription/', views.inscription_etudiant, name='inscription_etudiant'),
    path('student/verifier-email-etudiant',views.verifier_email_etudiant,name='verifier_email_etudiant'),
    path('student/connexion/', views.connexion_etudiant, name='connexion_etudiant'),
    path('student/deconnexion/', views.deconnexion_etudiant, name='deconnexion_etudiant'),
    path('student/dashboard/', views.dashboard_etudiant, name='dashboard_etudiant'),

    # Actions Étudiant
    path('student/inscrire-matiere/<int:matiere_id>/', views.inscription_matiere, name='inscription_matiere'),
    path('student/lien-inscription/', views.traiter_lien_inscription, name='traiter_lien_inscription'),
    path('student/valider-presence/', views.valider_presence, name='valider_presence'),
]