from django.core.management.base import BaseCommand
from appels.models import Ecole

class Command(BaseCommand):
    help = "Remplit la base de données avec les écoles principales du Cameroun"

    def handle(self, *args, **kwargs):
        ecoles_data = [
            {"nom": "École Nationale Supérieure des Travaux Publics", "abreviation": "ENSTP", "adresse": "Yaoundé"},
            {"nom": "École Nationale Supérieure Polytechnique", "abreviation": "ENSPY", "adresse": "Yaoundé"},
            {"nom": "Université de Yaoundé I", "abreviation": "UY1", "adresse": "Ngoa-Ekelle"},
            {"nom": "Université de Yaoundé II", "abreviation": "UY2", "adresse": "Soa"},
            {"nom": "Université Catholique d'Afrique Centrale", "abreviation": "UCAC", "adresse": "Yaoundé"},
            {"nom": "Institut Universitaire de Technologie de Douala", "abreviation": "IUT-D", "adresse": "Douala"},
        ]

        for data in ecoles_data:
            ecole, created = Ecole.objects.get_or_create(
                nom=data["nom"],
                defaults={"abreviation": data["abreviation"], "adresse": data["adresse"]}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"École créée : {ecole.abreviation}"))
            else:
                self.stdout.write(self.style.WARNING(f"L'école {ecole.abreviation} existe déjà"))
