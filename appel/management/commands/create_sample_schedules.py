from django.core.management.base import BaseCommand
from appel.models import ClassSchedule, Filiere


class Command(BaseCommand):
    help = 'Create sample class schedules for testing'

    def handle(self, *args, **options):
        # Get or create test filiere
        filiere, created = Filiere.objects.get_or_create(
            nom='Informatique',
            defaults={
                'description': 'Filiere d\'Informatique',
                'salle': 'A101'
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created filiere: {filiere.nom}'))

        # Define schedule data
        schedules = [
            # Monday
            {'day': 'Monday', 'start': '08:00', 'end': '10:00', 'subject': 'Python Avancé', 'prof': 'Dr. Martin', 'room': 'A101'},
            {'day': 'Monday', 'start': '10:30', 'end': '12:30', 'subject': 'Structures de Données', 'prof': 'Prof. Dupont', 'room': 'A102'},
            {'day': 'Monday', 'start': '14:00', 'end': '16:00', 'subject': 'Bases de Données', 'prof': 'Dr. Ahmed', 'room': 'B201'},
            # Tuesday
            {'day': 'Tuesday', 'start': '08:00', 'end': '10:00', 'subject': 'Mathématiques', 'prof': 'Prof. Laurent', 'room': 'A103'},
            {'day': 'Tuesday', 'start': '10:30', 'end': '12:30', 'subject': 'Web Development', 'prof': 'Dr. Sophie', 'room': 'A104'},
            # Wednesday
            {'day': 'Wednesday', 'start': '08:00', 'end': '10:00', 'subject': 'Algorithmes', 'prof': 'Prof. Moussa', 'room': 'B202'},
            {'day': 'Wednesday', 'start': '11:00', 'end': '13:00', 'subject': 'Sécurité Informatique', 'prof': 'Dr. Farah', 'room': 'A105'},
            # Thursday
            {'day': 'Thursday', 'start': '08:00', 'end': '10:00', 'subject': 'Design Patterns', 'prof': 'Prof. Hassan', 'room': 'C301'},
            {'day': 'Thursday', 'start': '10:30', 'end': '12:30', 'subject': 'Projet Intégrateur', 'prof': 'Dr. Zaki', 'room': 'Lab01'},
            # Friday
            {'day': 'Friday', 'start': '09:00', 'end': '11:00', 'subject': 'Présentation Projet', 'prof': 'Prof. Karim', 'room': 'Auditorium'},
        ]

        day_map = {
            'Monday': 'Monday',
            'Tuesday': 'Tuesday',
            'Wednesday': 'Wednesday',
            'Thursday': 'Thursday',
            'Friday': 'Friday',
        }

        count = 0
        for item in schedules:
            schedule, created = ClassSchedule.objects.get_or_create(
                filiere=filiere,
                day_of_week=day_map[item['day']],
                start_time=item['start'],
                end_time=item['end'],
                defaults={
                    'subject': item['subject'],
                    'professor': item['prof'],
                    'room': item['room'],
                }
            )
            if created:
                count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {count} class schedules for filiere: {filiere.nom}'
            )
        )
