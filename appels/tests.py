from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model
from.models import Ecole,Enseignant,Etudiant,FeuilleAppel,Matiere,Personne,Inscription

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