from datetime import timedelta

from django.conf import settings
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model
from.models import Ecole,Enseignant,Etudiant,FeuilleAppel,Matiere,Personne,Inscription,Presence

"""class TestAcceuil(TestCase):
    def setUp(self):
        #Préparation des utilisateurs de test (enseignant et étudiant).
        # Une école est nécessaire si tes modèles Enseignant/Etudiant y sont liés
        self.ecole = Ecole.objects.create(nom="ENSTP", abreviation="ENSTP")

        # Création d'un enseignant
        self.enseignant = Enseignant.objects.create_user(
            username="prof_test",
            password="password123",
            email="prof@test.com"
        )
        self.enseignant.ecole.add(self.ecole)

        # Création d'un étudiant
        self.etudiant = Etudiant.objects.create_user(
            username="etudiant_test",
            password="password123",
            email="etudiant@test.com",
            ecole=self.ecole
        )

    def test_accueil_visiteur_non_connecte(self):
        #Un utilisateur anonyme doit voir la page d'accueil HTML.
        # 1. On fait une requête GET sur l'accueil
        response = self.client.get(reverse('accueil'))
        
        # 2. On vérifie que le statut est 200 (Succès)
        self.assertEqual(response.status_code, 200)
        
        # 3. On vérifie que le bon template HTML est utilisé
        self.assertTemplateUsed(response, 'accueil.html')

    def test_accueil_redirection_enseignant(self):
        #Un enseignant connecté doit être redirigé vers son dashboard.
        # 1. On connecte l'enseignant
        self.client.login(username="prof_test", password="password123")
        
        # 2. On tente d'accéder à l'accueil
        response = self.client.get(reverse('accueil'))
        
        # 3. On vérifie qu'il est bien redirigé vers la vue 'dashboard'
        self.assertRedirects(response, reverse('dashboard'))

    def test_accueil_redirection_etudiant(self):
        #Un étudiant connecté doit être redirigé vers le dashboard étudiant.
        # 1. On connecte l'étudiant
        self.client.login(username="etudiant_test", password="password123")
        
        # 2. On tente d'accéder à l'accueil
        response = self.client.get(reverse('accueil'))
        
        # 3. On vérifie la redirection vers 'dashboard_etudiant'
        self.assertRedirects(response, reverse('dashboard_etudiant'))

Enseignant = get_user_model()

class TestInscriptionEnseignant(TestCase):
    def test_inscription_enseignant_affichage_formulaire(self):
        response = self.client.get(reverse('inscription_enseignant'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'enseignant/inscription_enseignant.html')
        self.assertIn('form',response.context)

    def test_inscription_enseignant_succes_post(self):
        response = self.client.post(reverse('inscription_enseignant'),{
            'username': 'prof_luc',
            'email': 'luc@attendo.cm',
            'last_name': 'Menga',
            'first_name': 'Luc',
            'specialite': 'Génie Civil',
            'telephone': '677777777',
            'sexe': 'M',
            'password': '123',
            'password_confirm': '123'
        })
        self.assertRedirects(response,reverse('dashboard'))
        self.assertTrue(Enseignant.objects.filter(username='prof_luc').exists())
        enseignant_cree = Enseignant.objects.get(username = 'prof_luc')
        self.assertNotEqual(enseignant_cree.password,'123')
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('Inscription reussi !',messages)

    def test_inscription_enseignant_echec_formulaire_invalide(self):
        response = self.client.post(reverse('inscription_enseignant'),{
            'username': '',  
            'email': 'luc_invalide@attendo.cm',
            'password': '123'
        })
        self.assertEqual(response.status_code,200)
        self.assertEqual(Enseignant.objects.count(),0)
        messages =[m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Erreur lors de l'inscription",messages)"""

class TestConnexionEnseignant(TestCase):

    def setUp(self):
        self.enseignant_user = Enseignant.objects.create_user(
            username='prof_luc',
            email='luc@attendo.cm',
            password='MonSuperPassword123',
            specialite='Génie Civil',
            telephone='677777777',
            sexe='M'
        )
        self.autre_user = Etudiant.objects.create_user(
            username='etudiant_jean',
            email='jean@attendo.cm',
            password='StudentPassword123'
        )

        self.url = reverse('connexion_enseignant')

    def test_connexion_affichage(self):
        response =  self.client.get(self.url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'enseignant/connexion.html')

    def test_connexion_enseignant_succes_username(self):
        response = self.client.post(self.url,{
            'username': 'prof_luc',
            'password': 'MonSuperPassword123'
        })
        self.assertRedirects(response,reverse('dashboard'))

    def test_connexion_enseignant_succes_email(self):
        response = self.client.post(self.url,{
            'username': 'luc@attendo.cm',
            'password': 'MonSuperPassword123'
        })
        self.assertRedirects(response,reverse('dashboard'))

    def test_connexion_mot_de_passe_incorrect(self):
        response = self.client.post(self.url, {
            'username': 'prof_luc',
            'password': 'MauvaisMotDePasse'
        })
        self.assertEqual(response.status_code, 200)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Identifiant ou mot de passe incorrect.", messages)

    def test_connexion_utilisateur_inexistant(self):
        response = self.client.post(self.url, {
            'username': 'fantome_user',
            'password': 'Password123'
        })
        self.assertEqual(response.status_code, 200)
        
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Identifiant ou mot de passe incorrect.", messages)

    def test_connexion_acces_refuse_non_enseignant(self):
        response = self.client.post(self.url, {
            'username': 'etudiant_jean',
            'password': 'StudentPassword123'
        })
        self.assertEqual(response.status_code, 200)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Accès refusé : vous n'êtes pas autorisés", messages)


MDP_PROF = 'MonSuperPassword123'
MDP_ETUDIANT = 'StudentPassword123'


class BaseAppelTestCase(TestCase):
    """Jeu de données commun : deux écoles, deux enseignants, deux étudiants et une matière."""

    def setUp(self):
        self.ecole = Ecole.objects.create(nom="Ecole Nationale des Travaux Publics", abreviation="ENSTP")
        self.autre_ecole = Ecole.objects.create(nom="Faculte des Sciences", abreviation="FS")

        self.prof = Enseignant.objects.create_user(
            username='prof_luc',
            email='luc@attendo.cm',
            password=MDP_PROF,
            last_name='Menga',
            first_name='Luc',
            specialite='Génie Civil',
            telephone='677777777',
            sexe='M'
        )
        self.prof.ecole.add(self.ecole)

        self.autre_prof = Enseignant.objects.create_user(
            username='prof_paul',
            email='paul@attendo.cm',
            password=MDP_PROF,
            last_name='Ekani',
            first_name='Paul',
            specialite='Mathematiques',
            sexe='M'
        )

        self.etudiant = Etudiant.objects.create_user(
            username='ETU001',
            email='jean@attendo.cm',
            password=MDP_ETUDIANT,
            last_name='Ngono',
            first_name='Jean',
            matricule='ETU001',
            ecole=self.ecole,
            sexe='M'
        )

        self.etudiant_autre_ecole = Etudiant.objects.create_user(
            username='ETU002',
            email='marie@attendo.cm',
            password=MDP_ETUDIANT,
            last_name='Abena',
            first_name='Marie',
            matricule='ETU002',
            ecole=self.autre_ecole,
            sexe='F'
        )

        self.matiere = Matiere.objects.create(
            nom='Beton arme',
            code='GC101',
            credit=4,
            description='Cours de beton arme',
            enseignant=self.prof,
            ecole=self.ecole
        )

    # --- Helpers ---------------------------------------------------------
    def connecter_prof(self, prof=None):
        prof = prof or self.prof
        self.client.force_login(Personne.objects.get(id=prof.id))

    def connecter_etudiant(self, etudiant=None):
        etudiant = etudiant or self.etudiant
        self.client.force_login(Personne.objects.get(id=etudiant.id))

    def inscrire(self, etudiant=None, matiere=None, nb_presences=0, nb_abscences=0):
        return Inscription.objects.create(
            etudiant=etudiant or self.etudiant,
            matiere=matiere or self.matiere,
            nb_presences=nb_presences,
            nb_abscences=nb_abscences
        )

    def creer_feuille_obj(self, matiere=None, **kwargs):
        return FeuilleAppel.objects.create(matiere=matiere or self.matiere, **kwargs)

    def messages_de(self, response):
        return [m.message for m in get_messages(response.wsgi_request)]


# =============================================================================
#   ACCUEIL
# =============================================================================
class TestAccueil(BaseAppelTestCase):

    def test_accueil_visiteur_non_connecte(self):
        response = self.client.get(reverse('accueil'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accueil.html')

    def test_accueil_redirige_enseignant_vers_dashboard(self):
        self.connecter_prof()
        response = self.client.get(reverse('accueil'))
        self.assertRedirects(response, reverse('dashboard'))

    def test_accueil_redirige_etudiant_vers_dashboard_etudiant(self):
        self.connecter_etudiant()
        response = self.client.get(reverse('accueil'))
        self.assertRedirects(response, reverse('dashboard_etudiant'))


# =============================================================================
#   ESPACE ENSEIGNANT : AUTHENTIFICATION
# =============================================================================
class TestInscriptionEnseignant(BaseAppelTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('inscription_enseignant')

    def test_affichage_formulaire(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'enseignant/inscription_enseignant.html')
        self.assertIn('form', response.context)

    def test_inscription_succes(self):
        response = self.client.post(self.url, {
            'username': 'prof_marc',
            'email': 'marc@attendo.cm',
            'last_name': 'Bello',
            'first_name': 'Marc',
            'specialite': 'Topographie',
            'telephone': '699999999',
            'sexe': 'M',
            'password': 'MotDePasseSolide123',
            'password_confirm': 'MotDePasseSolide123'
        })
        self.assertRedirects(response, reverse('dashboard'))
        nouveau = Enseignant.objects.get(username='prof_marc')
        self.assertNotEqual(nouveau.password, 'MotDePasseSolide123')
        self.assertTrue(nouveau.check_password('MotDePasseSolide123'))
        self.assertIn('Inscription reussi !', self.messages_de(response))

    def test_inscription_echec_mots_de_passe_differents(self):
        response = self.client.post(self.url, {
            'username': 'prof_marc',
            'email': 'marc@attendo.cm',
            'last_name': 'Bello',
            'first_name': 'Marc',
            'specialite': 'Topographie',
            'sexe': 'M',
            'password': 'MotDePasseSolide123',
            'password_confirm': 'AutreMotDePasse456'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Enseignant.objects.filter(username='prof_marc').exists())
        self.assertIn("Erreur lors de l'inscription", self.messages_de(response))

    def test_inscription_echec_champs_obligatoires_manquants(self):
        response = self.client.post(self.url, {
            'username': '',
            'email': 'incomplet@attendo.cm',
            'password': 'MotDePasseSolide123',
            'password_confirm': 'MotDePasseSolide123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Enseignant.objects.filter(email='incomplet@attendo.cm').exists())
        self.assertIn("Erreur lors de l'inscription", self.messages_de(response))


class TestDeconnexionEnseignant(BaseAppelTestCase):

    def test_deconnexion_redirige_vers_connexion(self):
        self.connecter_prof()
        response = self.client.get(reverse('deconnexion_enseignant'))
        self.assertRedirects(response, reverse('connexion_enseignant'))
        self.assertNotIn('_auth_user_id', self.client.session)


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class TestMotDePasseOublier(BaseAppelTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('mot_de_passe_oublier')

    def test_affichage_formulaire(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'enseignant/mot_de_passe_oublier.html')
        self.assertIn('form', response.context)

    def test_email_connu_envoie_un_code(self):
        response = self.client.post(self.url, {'email': self.prof.email})
        self.assertRedirects(response, reverse('verifier_code_recuperation'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.prof.email])
        self.assertEqual(self.client.session['reset_email'], self.prof.email)
        self.assertEqual(len(self.client.session['reset_code']), 6)

    def test_email_inconnu_affiche_une_erreur(self):
        response = self.client.post(self.url, {'email': 'inconnu@attendo.cm'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)
        self.assertNotIn('reset_email', self.client.session)
        self.assertIn(
            "Cet utilisateur n'existe pas ou n'est pas un enseignant verifier l'email",
            self.messages_de(response)
        )

    def test_email_invalide_ne_declenche_rien(self):
        response = self.client.post(self.url, {'email': 'pas-un-email'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)


class TestVerifierCodeRecuperation(BaseAppelTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('verifier_code_recuperation')

    def preparer_session(self, code='123456', code_verified=False):
        session = self.client.session
        session['reset_email'] = self.prof.email
        session['reset_code'] = code
        if code_verified:
            session['code_verified'] = True
        session.save()

    def test_sans_session_redirige_vers_mot_de_passe_oublier(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('mot_de_passe_oublier'))
        self.assertIn("Session expirée ou invalide. Veullez recommencer", self.messages_de(response))

    def test_affichage_etape_saisie_code(self):
        self.preparer_session()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'enseignant/verifier_code_recuperation.html')
        self.assertEqual(response.context['etape'], 'saisie_code')

    def test_code_incorrect(self):
        self.preparer_session(code='123456')
        response = self.client.post(self.url, {'code_saisi': '999999'})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('code_verified', self.client.session)
        self.assertIn("Code incorrect.Veuillez réesayer", self.messages_de(response))

    def test_code_correct_passe_a_l_etape_suivante(self):
        self.preparer_session(code='123456')
        response = self.client.post(self.url, {'code_saisi': '123456'})
        self.assertRedirects(response, self.url)
        self.assertTrue(self.client.session['code_verified'])

    def test_affichage_etape_nouveau_password(self):
        self.preparer_session(code_verified=True)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['etape'], 'nouveau_password')

    def test_reinitialisation_du_mot_de_passe(self):
        self.preparer_session(code_verified=True)
        response = self.client.post(self.url, {
            'password': 'NouveauPassword123',
            'confirm_password': 'NouveauPassword123'
        })
        self.assertRedirects(response, reverse('connexion_enseignant'))
        self.prof.refresh_from_db()
        self.assertTrue(self.prof.check_password('NouveauPassword123'))
        self.assertNotIn('reset_email', self.client.session)

    def test_nouveaux_mots_de_passe_differents(self):
        self.preparer_session(code_verified=True)
        response = self.client.post(self.url, {
            'password': 'NouveauPassword123',
            'confirm_password': 'PasLeMeme456'
        })
        self.assertEqual(response.status_code, 200)
        self.prof.refresh_from_db()
        self.assertTrue(self.prof.check_password(MDP_PROF))


class TestDashboardEnseignant(BaseAppelTestCase):

    def test_acces_refuse_si_non_connecte(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(settings.LOGIN_URL, response.url)
        self.assertIn(reverse('dashboard'), response.url)

    def test_dashboard_liste_les_matieres_du_prof(self):
        Matiere.objects.create(nom='Topographie', code='GC102', credit=3,
                               enseignant=self.autre_prof, ecole=self.ecole)
        self.connecter_prof()
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'enseignant/dashboard.html')
        self.assertQuerySetEqual(response.context['matieres'], [self.matiere])


# =============================================================================
#   ESPACE ENSEIGNANT : GESTION DES MATIERES
# =============================================================================
class TestCreerMatiere(BaseAppelTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('creer_matiere')

    def test_acces_refuse_si_non_connecte(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_affichage_formulaire(self):
        self.connecter_prof()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'enseignant/creer_matiere.html')
        self.assertIn('form', response.context)
        self.assertIn(self.ecole, response.context['ecoles_all'])

    def test_creation_matiere_simple(self):
        self.connecter_prof()
        response = self.client.post(self.url, {
            'nom': 'Hydraulique',
            'code': 'GC201',
            'credit': 5,
            'description': 'Cours hydraulique',
            'ecole': self.ecole.nom
        })
        self.assertRedirects(response, reverse('dashboard'))
        matiere = Matiere.objects.get(code='GC201')
        self.assertEqual(matiere.enseignant.id, self.prof.id)
        self.assertFalse(matiere.est_pondere)

    def test_creation_matiere_ponderee(self):
        self.connecter_prof()
        self.client.post(self.url, {
            'nom': 'Hydraulique',
            'code': 'GC201',
            'credit': 5,
            'ecole': self.ecole.nom,
            'est_pondere': 'on',
            'points_presence': '0.5',
            'points_absence': '-1'
        })
        matiere = Matiere.objects.get(code='GC201')
        self.assertTrue(matiere.est_pondere)
        self.assertEqual(matiere.points_presence, 0.5)
        self.assertEqual(matiere.points_absence, -1.0)

    def test_creation_echec_ecole_inexistante(self):
        self.connecter_prof()
        response = self.client.post(self.url, {
            'nom': 'Hydraulique',
            'code': 'GC201',
            'credit': 5,
            'ecole': 'Ecole Fantome'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Matiere.objects.filter(code='GC201').exists())

    def test_creation_echec_etudiant_connecte(self):
        self.connecter_etudiant()
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('connexion_enseignant'))
        self.assertIn("Seul les enseignant ont accèes à cette page", self.messages_de(response))


class TestModifierMatiere(BaseAppelTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('modifier_matiere', args=[self.matiere.id])

    def test_affichage_formulaire_prerempli(self):
        self.connecter_prof()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'enseignant/modifier_matiere.html')
        self.assertEqual(response.context['matiere'], self.matiere)

    def test_modification_succes(self):
        self.connecter_prof()
        response = self.client.post(self.url, {
            'nom': 'Beton precontrai',
            'code': 'GC199',
            'credit': 6,
            'description': 'Mise a jour',
            'ecole': self.ecole.nom
        })
        self.assertRedirects(response, reverse('dashboard'))
        self.matiere.refresh_from_db()
        self.assertEqual(self.matiere.nom, 'Beton precontrai')
        self.assertEqual(self.matiere.credit, 6)

    def test_modification_impossible_pour_un_autre_prof(self):
        self.connecter_prof(self.autre_prof)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)


class TestSupprimerMatiere(BaseAppelTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('supprimer_matiere', args=[self.matiere.id])

    def test_affichage_page_de_confirmation(self):
        self.connecter_prof()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'enseignant/supprimer_matiere.html')
        self.assertTrue(Matiere.objects.filter(id=self.matiere.id).exists())

    def test_suppression_effective_en_post(self):
        self.connecter_prof()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Matiere.objects.filter(id=self.matiere.id).exists())

    def test_suppression_impossible_pour_un_autre_prof(self):
        self.connecter_prof(self.autre_prof)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Matiere.objects.filter(id=self.matiere.id).exists())


class TestConsulterMatiere(BaseAppelTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('consulter_matiere', args=[self.matiere.id])

    def test_consultation_affiche_inscriptions_et_historique(self):
        self.inscrire(nb_presences=2, nb_abscences=1)
        self.creer_feuille_obj()
        self.connecter_prof()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'enseignant/consulter_matiere.html')
        self.assertEqual(len(response.context['inscriptions']), 1)
        self.assertEqual(response.context['nb_seances'], 1)

    def test_note_assiduite_calculee_si_matiere_ponderee(self):
        self.matiere.est_pondere = True
        self.matiere.points_presence = 1.0
        self.matiere.points_absence = -2.0
        self.matiere.save()
        inscription = self.inscrire()
        feuille = self.creer_feuille_obj()
        Presence.objects.create(feuille=feuille, etudiant=self.etudiant, est_present=True)
        self.connecter_prof()
        response = self.client.get(self.url)
        note = response.context['inscriptions'][0].note_actuelle
        self.assertEqual(note, 1.0)
        self.assertEqual(response.context['inscriptions'][0].id, inscription.id)

    def test_note_absente_si_matiere_non_ponderee(self):
        self.inscrire()
        self.connecter_prof()
        response = self.client.get(self.url)
        self.assertIsNone(response.context['inscriptions'][0].note_actuelle)

    def test_consultation_impossible_pour_un_autre_prof(self):
        self.connecter_prof(self.autre_prof)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)


class TestReinitialiserMatiere(BaseAppelTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('reinitialiser_matiere', args=[self.matiere.id])
        self.inscrire()
        self.feuille = self.creer_feuille_obj()
        Presence.objects.create(feuille=self.feuille, etudiant=self.etudiant, est_present=True)

    def test_reinitialisation_efface_tout(self):
        self.connecter_prof()
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('consulter_matiere', args=[self.matiere.id]))
        self.assertEqual(Presence.objects.filter(feuille__matiere=self.matiere).count(), 0)
        self.assertEqual(FeuilleAppel.objects.filter(matiere=self.matiere).count(), 0)
        self.assertEqual(Inscription.objects.filter(matiere=self.matiere).count(), 0)

    def test_get_ne_reinitialise_rien(self):
        self.connecter_prof()
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('consulter_matiere', args=[self.matiere.id]))
        self.assertEqual(Inscription.objects.filter(matiere=self.matiere).count(), 1)


class TestViderHistoriqueMatiere(BaseAppelTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('vider_historique_matiere', args=[self.matiere.id])
        self.inscription = self.inscrire(nb_presences=3, nb_abscences=2)
        self.creer_feuille_obj()

    def test_vider_historique_conserve_les_inscriptions(self):
        self.connecter_prof()
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('consulter_matiere', args=[self.matiere.id]))
        self.assertEqual(FeuilleAppel.objects.filter(matiere=self.matiere).count(), 0)
        self.inscription.refresh_from_db()
        self.assertEqual(self.inscription.nb_presences, 0)
        self.assertEqual(self.inscription.nb_abscences, 0)

    def test_get_ne_vide_rien(self):
        self.connecter_prof()
        self.client.get(self.url)
        self.assertEqual(FeuilleAppel.objects.filter(matiere=self.matiere).count(), 1)


# =============================================================================
#   ESPACE ENSEIGNANT : GESTION DES ETUDIANTS
# =============================================================================
class TestChercherEtudiant(BaseAppelTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('chercher_etudiant', args=[self.matiere.id])

    def test_recherche_sans_query(self):
        self.connecter_prof()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'enseignant/chercher_etudiant.html')
        self.assertIsNone(response.context['resultat'])
        self.assertIsNone(response.context['erreur'])

    def test_recherche_etudiant_trouve(self):
        self.connecter_prof()
        response = self.client.get(self.url, {'matricule': 'ETU001'})
        self.assertEqual(response.context['resultat'].id, self.etudiant.id)
        self.assertFalse(response.context['deja_inscrit'])

    def test_recherche_etudiant_deja_inscrit(self):
        self.inscrire()
        self.connecter_prof()
        response = self.client.get(self.url, {'matricule': 'ETU001'})
        self.assertTrue(response.context['deja_inscrit'])

    def test_recherche_etudiant_introuvable(self):
        self.connecter_prof()
        response = self.client.get(self.url, {'matricule': 'INCONNU'})
        self.assertIsNone(response.context['resultat'])
        self.assertEqual(response.context['erreur'], "Aucun étudiant trouver avec ce matricule")


class TestInscrireEtudiantParEnseignant(BaseAppelTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('inscrire_etudiant_par_ensei', args=[self.matiere.id, self.etudiant.id])

    def test_inscription_initialise_les_absences_avec_les_seances_passees(self):
        self.creer_feuille_obj()
        self.creer_feuille_obj()
        self.connecter_prof()
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('chercher_etudiant', args=[self.matiere.id]))
        inscription = Inscription.objects.get(etudiant=self.etudiant, matiere=self.matiere)
        self.assertEqual(inscription.nb_presences, 0)
        self.assertEqual(inscription.nb_abscences, 2)
        self.assertIn(f"{self.etudiant.first_name} est maintenant inscrit à {self.matiere.nom}",
                      self.messages_de(response))

    def test_double_inscription_ne_cree_pas_de_doublon(self):
        self.inscrire()
        self.connecter_prof()
        response = self.client.get(self.url)
        self.assertEqual(Inscription.objects.filter(etudiant=self.etudiant, matiere=self.matiere).count(), 1)
        self.assertIn(f"{self.etudiant.first_name} etait déja inscrit", self.messages_de(response))

    def test_inscription_impossible_pour_un_autre_prof(self):
        self.connecter_prof(self.autre_prof)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)


# =============================================================================
#   ESPACE ENSEIGNANT : APPEL
# =============================================================================
class TestCreerFeuille(BaseAppelTestCase):

    def test_creation_feuille_redirige_vers_faire_appel(self):
        self.connecter_prof()
        response = self.client.get(reverse('creer_feuille', args=[self.matiere.id]))
        feuille = FeuilleAppel.objects.get(matiere=self.matiere)
        self.assertRedirects(response, reverse('faire_appel', args=[feuille.id]))

    def test_creation_impossible_pour_un_autre_prof(self):
        self.connecter_prof(self.autre_prof)
        response = self.client.get(reverse('creer_feuille', args=[self.matiere.id]))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(FeuilleAppel.objects.count(), 0)


class TestFaireAppel(BaseAppelTestCase):

    def setUp(self):
        super().setUp()
        self.inscrire()
        self.feuille = self.creer_feuille_obj()
        self.url = reverse('faire_appel', args=[self.feuille.id])

    def test_affichage_feuille(self):
        self.connecter_prof()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'enseignant/faire_appel.html')
        self.assertEqual(response.context['feuille'], self.feuille)
        self.assertEqual(len(response.context['inscriptions']), 1)

    def test_cloture_automatique_quand_le_temps_est_ecoule(self):
        self.feuille.is_actif = True
        self.feuille.date_fin_appel = timezone.now() - timedelta(minutes=1)
        self.feuille.save()
        self.connecter_prof()
        response = self.client.get(self.url)
        self.feuille.refresh_from_db()
        self.assertFalse(self.feuille.is_actif)
        self.assertIn("Le temps est écoulé, l'appel a été clôturé automatiquement.",
                      self.messages_de(response))

    def test_detection_de_triche_sur_device_id_partage(self):
        autre_etudiant = Etudiant.objects.create_user(
            username='ETU003', email='paul.etu@attendo.cm', password=MDP_ETUDIANT,
            matricule='ETU003', ecole=self.ecole
        )
        self.inscrire(etudiant=autre_etudiant)
        Presence.objects.create(feuille=self.feuille, etudiant=self.etudiant,
                                est_present=True, device_id='MEME-TELEPHONE')
        Presence.objects.create(feuille=self.feuille, etudiant=autre_etudiant,
                                est_present=True, device_id='MEME-TELEPHONE')
        self.connecter_prof()
        response = self.client.get(self.url)
        self.assertIn('MEME-TELEPHONE', response.context['liste_tricheurs'])
        self.assertCountEqual(response.context['liste_tricheurs_ids'],
                              [self.etudiant.id, autre_etudiant.id])

    def test_acces_impossible_pour_un_autre_prof(self):
        self.connecter_prof(self.autre_prof)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)


class TestLancerAppel(BaseAppelTestCase):

    def setUp(self):
        super().setUp()
        self.inscrire()
        self.feuille = self.creer_feuille_obj()
        self.url = reverse('lancer_appel', args=[self.feuille.id])

    def test_lancement_genere_code_et_presences(self):
        self.connecter_prof()
        response = self.client.post(self.url, {
            'duree': 10,
            'rayon': 50,
            'lat_prof': '3.8480',
            'lon_prof': '11.5021'
        })
        self.assertRedirects(response, reverse('faire_appel', args=[self.feuille.id]))
        self.feuille.refresh_from_db()
        self.assertTrue(self.feuille.is_actif)
        self.assertTrue(self.feuille.appel_lance)
        self.assertEqual(len(self.feuille.code_validation), 6)
        self.assertEqual(self.feuille.rayon_autorise, 50)
        self.assertAlmostEqual(self.feuille.latitude_prof, 3.8480)
        self.assertAlmostEqual(self.feuille.longitude_prof, 11.5021)
        self.assertGreater(self.feuille.date_fin_appel, timezone.now())
        presence = Presence.objects.get(feuille=self.feuille, etudiant=self.etudiant)
        self.assertFalse(presence.est_present)

    def test_lancement_sans_gps(self):
        self.connecter_prof()
        self.client.post(self.url, {'duree': 5, 'rayon': 100, 'lat_prof': '', 'lon_prof': ''})
        self.feuille.refresh_from_db()
        self.assertIsNone(self.feuille.latitude_prof)
        self.assertIsNone(self.feuille.longitude_prof)

    def test_double_lancement_refuse(self):
        self.feuille.code_validation = '123456'
        self.feuille.save()
        self.connecter_prof()
        response = self.client.post(self.url, {'duree': 5, 'rayon': 100})
        self.assertRedirects(response, reverse('faire_appel', args=[self.feuille.id]))
        self.feuille.refresh_from_db()
        self.assertEqual(self.feuille.code_validation, '123456')
        self.assertIn("Cet appel a déjà été généré.", self.messages_de(response))

    def test_lancement_impossible_pour_un_autre_prof(self):
        self.connecter_prof(self.autre_prof)
        response = self.client.post(self.url, {'duree': 5, 'rayon': 100})
        self.assertEqual(response.status_code, 404)


class TestCloturerAppel(BaseAppelTestCase):

    def setUp(self):
        super().setUp()
        self.inscription = self.inscrire()
        self.feuille = self.creer_feuille_obj(is_actif=True)
        self.url = reverse('cloturer_appel', args=[self.feuille.id])

    def test_cloture_comptabilise_les_absences(self):
        Presence.objects.create(feuille=self.feuille, etudiant=self.etudiant, est_present=False)
        self.connecter_prof()
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('faire_appel', args=[self.feuille.id]))
        self.feuille.refresh_from_db()
        self.inscription.refresh_from_db()
        self.assertFalse(self.feuille.is_actif)
        self.assertEqual(self.inscription.nb_abscences, 1)

    def test_cloture_ne_penalise_pas_les_presents(self):
        Presence.objects.create(feuille=self.feuille, etudiant=self.etudiant, est_present=True)
        self.connecter_prof()
        self.client.post(self.url)
        self.inscription.refresh_from_db()
        self.assertEqual(self.inscription.nb_abscences, 0)

    def test_cloture_impossible_pour_un_autre_prof(self):
        self.connecter_prof(self.autre_prof)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)


class TestMarquerPresence(BaseAppelTestCase):

    def setUp(self):
        super().setUp()
        self.inscription = self.inscrire()
        self.feuille = self.creer_feuille_obj()

    def url_statut(self, statut):
        return reverse('marquer_presence', args=[self.feuille.id, self.etudiant.id, statut])

    def test_marquer_present(self):
        self.connecter_prof()
        response = self.client.get(self.url_statut('present'))
        self.assertRedirects(response, reverse('faire_appel', args=[self.feuille.id]))
        self.inscription.refresh_from_db()
        self.assertEqual(self.inscription.nb_presences, 1)
        self.assertTrue(Presence.objects.get(feuille=self.feuille, etudiant=self.etudiant).est_present)

    def test_marquer_absent(self):
        self.connecter_prof()
        self.client.get(self.url_statut('abscent'))
        self.inscription.refresh_from_db()
        self.assertEqual(self.inscription.nb_abscences, 1)
        self.assertFalse(Presence.objects.get(feuille=self.feuille, etudiant=self.etudiant).est_present)

    def test_annuler_une_presence(self):
        self.connecter_prof()
        self.client.get(self.url_statut('present'))
        self.client.get(self.url_statut('annulerP'))
        self.inscription.refresh_from_db()
        self.assertEqual(self.inscription.nb_presences, 0)
        self.assertFalse(Presence.objects.filter(feuille=self.feuille, etudiant=self.etudiant).exists())

    def test_annuler_une_absence(self):
        self.connecter_prof()
        self.client.get(self.url_statut('abscent'))
        self.client.get(self.url_statut('annulerA'))
        self.inscription.refresh_from_db()
        self.assertEqual(self.inscription.nb_abscences, 0)

    def test_annulation_sans_compteur_ne_descend_pas_sous_zero(self):
        self.connecter_prof()
        self.client.get(self.url_statut('annulerP'))
        self.inscription.refresh_from_db()
        self.assertEqual(self.inscription.nb_presences, 0)

    def test_marquage_impossible_si_etudiant_non_inscrit(self):
        self.inscription.delete()
        self.connecter_prof()
        response = self.client.get(self.url_statut('present'))
        self.assertEqual(response.status_code, 404)

    def test_marquage_impossible_pour_un_autre_prof(self):
        self.connecter_prof(self.autre_prof)
        response = self.client.get(self.url_statut('present'))
        self.assertEqual(response.status_code, 404)


class TestConsulterFeuille(BaseAppelTestCase):

    def setUp(self):
        super().setUp()
        self.feuille = self.creer_feuille_obj()
        self.url = reverse('consulter_feuille', args=[self.feuille.id])

    def test_affichage_des_pointages(self):
        Presence.objects.create(feuille=self.feuille, etudiant=self.etudiant, est_present=True)
        self.connecter_prof()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'enseignant/consulter_feuille.html')
        self.assertEqual(len(response.context['pointages']), 1)
        self.assertEqual(response.context['matiere'], self.matiere)

    def test_consultation_impossible_pour_un_autre_prof(self):
        self.connecter_prof(self.autre_prof)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)


class TestSupprimerFeuille(BaseAppelTestCase):

    def setUp(self):
        super().setUp()
        self.inscription = self.inscrire(nb_presences=1, nb_abscences=1)
        self.feuille = self.creer_feuille_obj()
        self.url = reverse('supprimer_feuille', args=[self.feuille.id])

    def test_suppression_decremente_les_presences(self):
        Presence.objects.create(feuille=self.feuille, etudiant=self.etudiant, est_present=True)
        self.connecter_prof()
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('consulter_matiere', args=[self.matiere.id]))
        self.assertFalse(FeuilleAppel.objects.filter(id=self.feuille.id).exists())
        self.inscription.refresh_from_db()
        self.assertEqual(self.inscription.nb_presences, 0)
        self.assertEqual(self.inscription.nb_abscences, 1)

    def test_suppression_decremente_les_absences(self):
        Presence.objects.create(feuille=self.feuille, etudiant=self.etudiant, est_present=False)
        self.connecter_prof()
        self.client.post(self.url)
        self.inscription.refresh_from_db()
        self.assertEqual(self.inscription.nb_presences, 1)
        self.assertEqual(self.inscription.nb_abscences, 0)

    def test_suppression_impossible_pour_un_autre_prof(self):
        self.connecter_prof(self.autre_prof)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(FeuilleAppel.objects.filter(id=self.feuille.id).exists())


# =============================================================================
#   ESPACE ENSEIGNANT : EXPORTS PDF
# =============================================================================
class TestExportsPdf(BaseAppelTestCase):

    def setUp(self):
        super().setUp()
        self.inscrire(nb_presences=1)
        self.feuille = self.creer_feuille_obj()
        Presence.objects.create(feuille=self.feuille, etudiant=self.etudiant, est_present=True)

    def test_export_feuille_pdf(self):
        self.connecter_prof()
        response = self.client.get(reverse('exporter_pdf', args=[self.feuille.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('attachment;', response['Content-Disposition'])
        self.assertTrue(response.content.startswith(b'%PDF'))

    def test_export_feuille_pdf_filtre_absents(self):
        self.connecter_prof()
        response = self.client.get(reverse('exporter_pdf', args=[self.feuille.id]), {'filtre': 'absent'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('absent', response['Content-Disposition'])

    def test_export_feuille_pdf_impossible_pour_un_autre_prof(self):
        self.connecter_prof(self.autre_prof)
        response = self.client.get(reverse('exporter_pdf', args=[self.feuille.id]))
        self.assertEqual(response.status_code, 404)

    def test_export_bilan_matiere_pdf(self):
        self.matiere.est_pondere = True
        self.matiere.points_presence = 1.0
        self.matiere.points_absence = -1.0
        self.matiere.save()
        self.connecter_prof()
        response = self.client.get(reverse('exporter_bilan_pdf', args=[self.matiere.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue(response.content.startswith(b'%PDF'))

    def test_export_bilan_impossible_pour_un_autre_prof(self):
        self.connecter_prof(self.autre_prof)
        response = self.client.get(reverse('exporter_bilan_pdf', args=[self.matiere.id]))
        self.assertEqual(response.status_code, 404)


# =============================================================================
#   ESPACE ETUDIANT : AUTHENTIFICATION
# =============================================================================
class TestInscriptionEtudiant(BaseAppelTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('inscription_etudiant')

    def test_affichage_formulaire(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'etudiant/inscription_etudiant.html')
        self.assertIn('form', response.context)
        self.assertIn(self.ecole, response.context['ecoles_all'])

    def test_inscription_succes(self):
        response = self.client.post(self.url, {
            'username': 'ETU100',
            'last_name': 'Fotso',
            'first_name': 'Alice',
            'ecole': self.ecole.nom,
            'email': 'alice@attendo.cm',
            'telephone': '655555555',
            'sexe': 'F',
            'password': 'PasswordEtudiant123',
            'password_confirm': 'PasswordEtudiant123'
        })
        self.assertRedirects(response, reverse('dashboard_etudiant'))
        etudiant = Etudiant.objects.get(username='ETU100')
        self.assertEqual(etudiant.matricule, 'ETU100')
        self.assertEqual(etudiant.ecole, self.ecole)
        self.assertTrue(etudiant.check_password('PasswordEtudiant123'))

    def test_inscription_echec_mots_de_passe_differents(self):
        response = self.client.post(self.url, {
            'username': 'ETU100',
            'last_name': 'Fotso',
            'first_name': 'Alice',
            'ecole': self.ecole.nom,
            'email': 'alice@attendo.cm',
            'sexe': 'F',
            'password': 'PasswordEtudiant123',
            'password_confirm': 'AutreChose456'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Etudiant.objects.filter(username='ETU100').exists())

    def test_inscription_echec_ecole_inexistante(self):
        response = self.client.post(self.url, {
            'username': 'ETU100',
            'last_name': 'Fotso',
            'first_name': 'Alice',
            'ecole': 'Ecole Fantome',
            'email': 'alice@attendo.cm',
            'sexe': 'F',
            'password': 'PasswordEtudiant123',
            'password_confirm': 'PasswordEtudiant123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Etudiant.objects.filter(username='ETU100').exists())


class TestConnexionEtudiant(BaseAppelTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('connexion_etudiant')

    def test_affichage_formulaire(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'etudiant/connexion_etudiant.html')

    def test_etudiant_deja_connecte_est_redirige(self):
        self.connecter_etudiant()
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('dashboard_etudiant'))

    def test_connexion_par_matricule(self):
        response = self.client.post(self.url, {'username': 'ETU001'})
        self.assertRedirects(response, reverse('dashboard_etudiant'))
        self.assertEqual(int(self.client.session['_auth_user_id']), self.etudiant.id)

    def test_connexion_par_email(self):
        response = self.client.post(self.url, {'username': 'jean@attendo.cm'})
        self.assertRedirects(response, reverse('dashboard_etudiant'))

    def test_connexion_refusee_pour_un_enseignant(self):
        response = self.client.post(self.url, {'username': 'prof_luc'})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Accès refusé : vous n'êtes pas autorisés", self.messages_de(response))

    def test_connexion_utilisateur_inexistant(self):
        response = self.client.post(self.url, {'username': 'FANTOME'})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)


class TestDeconnexionEtudiant(BaseAppelTestCase):

    def test_deconnexion_redirige_vers_connexion_etudiant(self):
        self.connecter_etudiant()
        response = self.client.get(reverse('deconnexion_etudiant'))
        self.assertRedirects(response, reverse('connexion_etudiant'))
        self.assertNotIn('_auth_user_id', self.client.session)


class TestDashboardEtudiant(BaseAppelTestCase):

    def test_dashboard_liste_les_inscriptions(self):
        self.inscrire(nb_presences=3, nb_abscences=1)
        self.connecter_etudiant()
        response = self.client.get(reverse('dashboard_etudiant'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'etudiant/dashboard_etudiant.html')
        self.assertEqual(len(response.context['inscriptions']), 1)
        self.assertEqual(response.context['etudiant'].id, self.etudiant.id)
        self.assertEqual(response.context['inscriptions'][0].taux_presence, 75.0)


# =============================================================================
#   ESPACE ETUDIANT : INSCRIPTION A UNE MATIERE
# =============================================================================
class TestInscriptionMatiere(BaseAppelTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('inscription_matiere', args=[self.matiere.id])

    def test_inscription_succes(self):
        self.creer_feuille_obj()
        self.connecter_etudiant()
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('dashboard_etudiant'))
        inscription = Inscription.objects.get(etudiant=self.etudiant, matiere=self.matiere)
        self.assertEqual(inscription.nb_abscences, 1)
        self.assertIn(f"Felicitations : tu es maintenant inscrire au cour de {self.matiere.nom}",
                      self.messages_de(response))

    def test_double_inscription(self):
        self.inscrire()
        self.connecter_etudiant()
        response = self.client.get(self.url)
        self.assertEqual(Inscription.objects.filter(etudiant=self.etudiant, matiere=self.matiere).count(), 1)
        self.assertIn(f"Tu es déja inscrit au cour de {self.matiere.nom}", self.messages_de(response))

    def test_inscription_refusee_si_autre_ecole(self):
        self.connecter_etudiant(self.etudiant_autre_ecole)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('dashboard_etudiant'))
        self.assertFalse(Inscription.objects.filter(etudiant=self.etudiant_autre_ecole).exists())
        self.assertIn("Accès refusé : vous ne faites pas partie de cette ecole.",
                      self.messages_de(response))

    def test_inscription_refusee_pour_un_enseignant(self):
        self.connecter_prof()
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('accueil'), target_status_code=302)
        self.assertIn("Accès refusé : tu n'as pas de profil étudiant.", self.messages_de(response))

    def test_matiere_inexistante(self):
        self.connecter_etudiant()
        response = self.client.get(reverse('inscription_matiere', args=[9999]))
        self.assertEqual(response.status_code, 404)


class TestTraiterLienInscription(BaseAppelTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('traiter_lien_inscription')

    def test_lien_valide_redirige_vers_inscription_matiere(self):
        self.connecter_etudiant()
        lien = f"http://127.0.0.1:8000/student/inscrire-matiere/{self.matiere.id}/"
        response = self.client.post(self.url, {'lien_complet': lien})
        self.assertRedirects(
            response,
            reverse('inscription_matiere', args=[self.matiere.id]),
            target_status_code=302
        )

    def test_lien_invalide(self):
        self.connecter_etudiant()
        response = self.client.post(self.url, {'lien_complet': 'http://127.0.0.1:8000/pro/dashboard/'})
        self.assertRedirects(response, reverse('dashboard_etudiant'))
        self.assertIn("Format du lien invalide ou non autorisé.", self.messages_de(response))

    def test_get_redirige_vers_dashboard(self):
        self.connecter_etudiant()
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('dashboard_etudiant'))


# =============================================================================
#   ESPACE ETUDIANT : VALIDATION DE PRESENCE
# =============================================================================
class TestValiderPresence(BaseAppelTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('valider_presence')
        self.inscription = self.inscrire()
        self.feuille = self.creer_feuille_obj(
            is_actif=True,
            appel_lance=True,
            code_validation='123456',
            date_fin_appel=timezone.now() + timedelta(minutes=5)
        )
        self.presence = Presence.objects.create(
            feuille=self.feuille, etudiant=self.etudiant, est_present=False
        )
        self.connecter_etudiant()

    def test_validation_succes_sans_gps(self):
        response = self.client.post(self.url, {
            'feuille_id': self.feuille.id,
            'code_saisi': '123456'
        })
        self.assertRedirects(response, reverse('dashboard_etudiant'))
        self.presence.refresh_from_db()
        self.inscription.refresh_from_db()
        self.assertTrue(self.presence.est_present)
        self.assertEqual(self.inscription.nb_presences, 1)

    def test_validation_enregistre_le_device_id(self):
        self.client.post(self.url, {
            'feuille_id': self.feuille.id,
            'code_saisi': '123456'
        }, HTTP_USER_AGENT='TelephoneDeJean/1.0')
        self.presence.refresh_from_db()
        self.assertEqual(self.presence.device_id, 'TelephoneDeJean/1.0')

    def test_code_incorrect(self):
        response = self.client.post(self.url, {
            'feuille_id': self.feuille.id,
            'code_saisi': '000000'
        })
        self.presence.refresh_from_db()
        self.assertFalse(self.presence.est_present)
        self.assertIn("code incorrect ou session expirée.", self.messages_de(response))

    def test_appel_termine(self):
        self.feuille.date_fin_appel = timezone.now() - timedelta(minutes=1)
        self.feuille.save()
        response = self.client.post(self.url, {
            'feuille_id': self.feuille.id,
            'code_saisi': '123456'
        })
        self.presence.refresh_from_db()
        self.assertFalse(self.presence.est_present)
        self.assertIn("Désolé l'appel est terminé veuillez consulter votre enseignant.",
                      self.messages_de(response))

    def test_deja_marque_present(self):
        self.presence.est_present = True
        self.presence.save()
        response = self.client.post(self.url, {
            'feuille_id': self.feuille.id,
            'code_saisi': '123456'
        })
        self.inscription.refresh_from_db()
        self.assertEqual(self.inscription.nb_presences, 0)
        self.assertIn("Tu es déjà marqué(e) present", self.messages_de(response))

    def test_gps_requis_si_le_prof_a_defini_une_zone(self):
        self.feuille.latitude_prof = 3.8480
        self.feuille.longitude_prof = 11.5021
        self.feuille.rayon_autorise = 100
        self.feuille.save()
        response = self.client.post(self.url, {
            'feuille_id': self.feuille.id,
            'code_saisi': '123456'
        })
        self.presence.refresh_from_db()
        self.assertFalse(self.presence.est_present)
        self.assertIn("Localisation GPS requise pour valider.", self.messages_de(response))

    def test_etudiant_dans_le_rayon(self):
        self.feuille.latitude_prof = 3.8480
        self.feuille.longitude_prof = 11.5021
        self.feuille.rayon_autorise = 100
        self.feuille.save()
        self.client.post(self.url, {
            'feuille_id': self.feuille.id,
            'code_saisi': '123456',
            'lat_etudiant': '3.84805',
            'lon_etudiant': '11.50215'
        })
        self.presence.refresh_from_db()
        self.assertTrue(self.presence.est_present)

    def test_etudiant_trop_loin(self):
        self.feuille.latitude_prof = 3.8480
        self.feuille.longitude_prof = 11.5021
        self.feuille.rayon_autorise = 50
        self.feuille.save()
        response = self.client.post(self.url, {
            'feuille_id': self.feuille.id,
            'code_saisi': '123456',
            'lat_etudiant': '4.0500',
            'lon_etudiant': '9.7000'
        })
        self.presence.refresh_from_db()
        self.assertFalse(self.presence.est_present)
        self.assertTrue(any(m.startswith("Tu es trop loin de l'enseignant")
                            for m in self.messages_de(response)))

    def test_get_redirige_sans_rien_valider(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('dashboard_etudiant'))
        self.presence.refresh_from_db()
        self.assertFalse(self.presence.est_present)