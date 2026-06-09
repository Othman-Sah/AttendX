import datetime
import random
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.models import User
from django.utils.timezone import make_aware
from django.utils import timezone

from appel.models import (
    Filiere,
    Etudiant,
    Presence,
    AbsenceJustification,
    DocumentRequest,
    ClassSchedule,
    Notification
)

class Command(BaseCommand):
    help = 'Seeds the database with realistic school data for testing AttendX'

    def handle(self, *args, **options):
        self.stdout.write("Starting to seed database...")

        # Ensure random seeding is reproducible but dynamic enough
        random.seed(42)

        try:
            with transaction.atomic():
                # 1. Clear old data
                self.stdout.write("Clearing existing non-superuser data...")
                Notification.objects.all().delete()
                DocumentRequest.objects.all().delete()
                AbsenceJustification.objects.all().delete()
                Presence.objects.all().delete()
                ClassSchedule.objects.all().delete()
                Etudiant.objects.all().delete()
                Filiere.objects.all().delete()
                
                # Delete non-superuser users
                User.objects.filter(is_superuser=False).delete()
                self.stdout.write("Existing data cleared.")

                # 2. Seed Teachers & Admin
                self.stdout.write("Seeding admin and teachers...")
                
                # Ensure admin exists and has password admin1234
                admin_user, admin_created = User.objects.get_or_create(
                    username='admin',
                    defaults={
                        'email': 'admin@example.com',
                        'is_superuser': True,
                        'is_staff': True
                    }
                )
                admin_user.set_password('admin1234')
                admin_user.is_superuser = True
                admin_user.is_staff = True
                admin_user.save()

                othman = User.objects.create_user(
                    username='othman',
                    email='othman@example.com',
                    first_name='Othman',
                    last_name='Benjelloun'
                )
                othman.set_password('prof1234')
                othman.save()

                prof = User.objects.create_user(
                    username='prof',
                    email='prof@example.com',
                    first_name='Professeur',
                    last_name='Amrani'
                )
                prof.set_password('prof1234')
                prof.save()

                self.stdout.write(f"Created admin and teachers: {admin_user.username}, {othman.username}, {prof.username}")

                # 3. Seed Filieres (Majors)
                self.stdout.write("Seeding majors (filieres)...")
                f_gl = Filiere.objects.create(
                    nom='Génie Logiciel',
                    description='Filière spécialisée dans le génie logiciel, le développement web, mobile et DevOps.',
                    salle='Salle A101',
                    teacher=othman
                )

                f_ia = Filiere.objects.create(
                    nom='Intelligence Artificielle',
                    description='Filière axée sur le Machine Learning, le Deep Learning et la Data Science.',
                    salle='Salle A102',
                    teacher=othman
                )

                f_sr = Filiere.objects.create(
                    nom='Systèmes & Réseaux',
                    description='Filière spécialisée dans l\'administration des systèmes Linux, le routage IP et le cloud computing.',
                    salle='Salle B201',
                    teacher=prof
                )

                f_cs = Filiere.objects.create(
                    nom='Cybersécurité',
                    description='Filière dédiée à la sécurité des systèmes d\'information, la cryptographie et le pentesting.',
                    salle='Salle B202',
                    teacher=prof
                )

                self.stdout.write("Created 4 majors (Génie Logiciel, Intelligence Artificielle, Systèmes & Réseaux, Cybersécurité)")

                # 4. Student Name Pool
                student_names = [
                    # Génie Logiciel (15)
                    ("Youssef", "Alami"), ("Sofia", "Bensouda"), ("Karim", "Amrani"),
                    ("Salma", "Idrissi"), ("Mehdi", "Tazi"), ("Chaimae", "Filali"),
                    ("Anass", "Mezouar"), ("Lina", "Cherkaoui"), ("Hamza", "Alaoui"),
                    ("Yasmina", "Jouahri"), ("Omar", "Radi"), ("Zineb", "Berrada"),
                    ("Nabil", "Fassi"), ("Kenza", "Kabbaj"), ("Tariq", "Mansouri"),
                    # Intelligence Artificielle (15)
                    ("Ghita", "Bennani"), ("Saad", "El Glaoui"), ("Sarah", "Lahlou"),
                    ("Adam", "Chraibi"), ("Meriem", "Naciri"), ("Walid", "Belkhayat"),
                    ("Ines", "Lahbabi"), ("Rayan", "Slaoui"), ("Rania", "Taziki"),
                    ("Hajar", "Senhaji"), ("Reda", "Mernissi"), ("Malak", "Guedira"),
                    ("Ayoub", "Guessous"), ("Driss", "El Harki"), ("Amina", "Bouazza"),
                    # Systèmes & Réseaux (15)
                    ("Othmane", "Sabiri"), ("Leila", "Jaber"), ("Jalal", "Kettani"),
                    ("Yousra", "Hajji"), ("Adil", "Harrak"), ("Noura", "Bennis"),
                    ("Bilal", "Sekkat"), ("Iman", "Zouari"), ("Mourad", "Sebti"),
                    ("Nada", "Regragui"), ("Zakaria", "El Fassi"), ("Hiba", "Outaleb"),
                    ("Yassine", "Oudghiri"), ("Khaoula", "Daoudi"), ("Younes", "Jabri"),
                    # Cybersécurité (15)
                    ("Rim", "Guessous"), ("Sami", "Skali"), ("Assia", "Tahiri"),
                    ("Farouk", "Mounir"), ("Salia", "Zehar"), ("Nizar", "Chaoui"),
                    ("Lamia", "Lahlou"), ("Badr", "El Amin"), ("Safae", "Mrini"),
                    ("Jawad", "Rhazi"), ("Dounia", "Berrada"), ("Tarik", "Benjelloun"),
                    ("Fatine", "Mansouri"), ("Khalid", "Sefrioui"), ("Soukaina", "Chraibi")
                ]

                # Assign names to filieres
                filiere_mapping = [
                    (f_gl, student_names[0:15]),
                    (f_ia, student_names[15:30]),
                    (f_sr, student_names[30:45]),
                    (f_cs, student_names[45:60])
                ]

                all_students = []
                student_counter = 1

                self.stdout.write("Seeding students and creating student portals...")
                for filiere, names in filiere_mapping:
                    for idx, (first_name, last_name) in enumerate(names):
                        full_name = f"{first_name} {last_name}"
                        username = f"{first_name.lower()}.{last_name.lower()}"
                        email = f"{username}@example.com"
                        num_etudiant = f"EST-2026-{student_counter:04d}"
                        
                        student_user = None
                        # Create User account for the first 3 students of each filiere
                        if idx < 3:
                            student_user = User.objects.create_user(
                                username=username,
                                email=email,
                                first_name=first_name,
                                last_name=last_name
                            )
                            student_user.set_password('student1234')
                            student_user.save()

                        student = Etudiant.objects.create(
                            user=student_user,
                            nom=full_name,
                            email=email,
                            numero_etudiant=num_etudiant,
                            filiere=filiere
                        )
                        all_students.append(student)
                        student_counter += 1

                self.stdout.write(f"Seeded {len(all_students)} students. Created {12} student portal logins.")

                # 5. Seed Class Schedules
                self.stdout.write("Seeding class schedules...")
                schedules_data = {
                    f_gl: [
                        ('Monday', '09:00:00', '11:30:00', 'Python Avancé', 'Dr. Benjelloun', 'Salle A101'),
                        ('Tuesday', '14:00:00', '16:30:00', 'Design Patterns', 'Dr. Benjelloun', 'Salle A101'),
                        ('Wednesday', '09:00:00', '11:30:00', 'Génie Logiciel & DevOps', 'Dr. Benjelloun', 'Salle A101'),
                        ('Friday', '10:00:00', '12:30:00', 'Bases de Données Relationnelles', 'Dr. Benjelloun', 'Salle A101')
                    ],
                    f_ia: [
                        ('Monday', '14:00:00', '16:30:00', 'Introduction au Machine Learning', 'Dr. Benjelloun', 'Salle A102'),
                        ('Wednesday', '14:00:00', '16:30:00', 'Réseaux de Neurones', 'Dr. Benjelloun', 'Salle A102'),
                        ('Thursday', '09:00:00', '11:30:00', 'Mathématiques pour l\'IA', 'Dr. Benjelloun', 'Salle A102'),
                        ('Friday', '14:00:00', '16:30:00', 'Python pour la Data Science', 'Dr. Benjelloun', 'Salle A102')
                    ],
                    f_sr: [
                        ('Monday', '09:00:00', '11:30:00', 'Administration Système Linux', 'Prof. Amrani', 'Salle B201'),
                        ('Tuesday', '09:00:00', '11:30:00', 'Réseaux IP et Routage', 'Prof. Amrani', 'Salle B201'),
                        ('Thursday', '14:00:00', '16:30:00', 'Services Réseaux & DNS', 'Prof. Amrani', 'Salle B201'),
                        ('Friday', '09:00:00', '11:30:00', 'Virtualisation & Cloud', 'Prof. Amrani', 'Salle B201')
                    ],
                    f_cs: [
                        ('Tuesday', '14:00:00', '16:30:00', 'Cryptographie Appliquée', 'Prof. Amrani', 'Salle B202'),
                        ('Wednesday', '09:00:00', '11:30:00', 'Sécurité des Réseaux', 'Prof. Amrani', 'Salle B202'),
                        ('Thursday', '09:00:00', '11:30:00', 'Pentesting & Audit', 'Prof. Amrani', 'Salle B202'),
                        ('Friday', '14:00:00', '16:30:00', 'Sécurité des OS', 'Prof. Amrani', 'Salle B202')
                    ]
                }

                schedule_count = 0
                for filiere, classes in schedules_data.items():
                    for day, start, end, subject, prof_name, room in classes:
                        ClassSchedule.objects.create(
                            filiere=filiere,
                            day_of_week=day,
                            start_time=start,
                            end_time=end,
                            subject=subject,
                            professor=prof_name,
                            room=room
                        )
                        schedule_count += 1
                self.stdout.write(f"Seeded {schedule_count} weekly class schedule slots.")

                # 6. Seed Weekday Presence History for the Past 30 Days
                self.stdout.write("Seeding daily attendance (last 30 days)...")
                today = timezone.localdate()
                absences_to_justify = []

                for days_ago in range(30, -1, -1):
                    current_date = today - datetime.timedelta(days=days_ago)
                    # Skip Sundays (standard rest day)
                    if current_date.weekday() == 6:
                        continue

                    # For each student, generate a presence record
                    for student in all_students:
                        # 88% chance of being present, 12% chance of being absent
                        is_present = random.random() > 0.12
                        
                        presence = Presence.objects.create(
                            etudiant=student,
                            date=current_date,
                            present=is_present
                        )

                        if not is_present:
                            absences_to_justify.append(presence)

                # Update counters on students
                for student in all_students:
                    student.refresh_attendance_totals(save=True)

                self.stdout.write(f"Seeded daily attendance records. Total absences recorded: {len(absences_to_justify)}")

                # 7. Seed Absence Justifications
                self.stdout.write("Seeding justifications...")
                # Select ~25% of absences to have justifications
                random.shuffle(absences_to_justify)
                justified_subset = absences_to_justify[:int(len(absences_to_justify) * 0.25)]

                justification_reasons = [
                    ("Certificat médical pour grippe saisonnière", "Veuillez trouver ci-joint mon certificat médical prescrivant un repos de 48 heures pour grippe."),
                    ("Panne de transport en commun", "Le tramway reliant mon domicile à l'université a subi une panne majeure ce matin, m'empêchant de venir en cours à temps."),
                    ("Rendez-vous médical spécialiste", "J'avais un rendez-vous planifié depuis 3 mois chez l'ophtalmologue que je ne pouvais pas reporter."),
                    ("Problème de santé mineur", "J'ai eu une intoxication alimentaire sévère hier soir et je n'étais pas en état de me déplacer."),
                    ("Urgence familiale", "J'ai dû assister un membre de ma famille proche pour une hospitalisation d'urgence ce matin.")
                ]

                justification_count = 0
                for idx, presence in enumerate(justified_subset):
                    reason, details = random.choice(justification_reasons)
                    
                    # Distribute status: 40% pending, 40% approved, 20% rejected
                    r = random.random()
                    if r < 0.40:
                        status = AbsenceJustification.STATUS_PENDING
                        teacher_comment = ""
                        reviewed_by = None
                        reviewed_at = None
                    elif r < 0.80:
                        status = AbsenceJustification.STATUS_APPROVED
                        teacher_comment = "Justificatif accepté. Bon rétablissement."
                        reviewed_by = presence.etudiant.filiere.teacher
                        reviewed_at = timezone.now() - datetime.timedelta(hours=random.randint(1, 48))
                    else:
                        status = AbsenceJustification.STATUS_REJECTED
                        teacher_comment = "Motif non valable ou justificatif officiel manquant. Veuillez fournir un certificat valide."
                        reviewed_by = presence.etudiant.filiere.teacher
                        reviewed_at = timezone.now() - datetime.timedelta(hours=random.randint(1, 48))

                    AbsenceJustification.objects.create(
                        presence=presence,
                        reason=reason,
                        details=details,
                        status=status,
                        teacher_comment=teacher_comment,
                        reviewed_by=reviewed_by,
                        reviewed_at=reviewed_at
                    )
                    justification_count += 1

                self.stdout.write(f"Seeded {justification_count} absence justification requests.")

                # 8. Seed Document Requests
                self.stdout.write("Seeding document requests...")
                doc_types = [
                    "Attestation de scolarité",
                    "Relevé de notes - Semestre 1",
                    "Lettre de recommandation académique",
                    "Convention de stage"
                ]

                doc_request_count = 0
                # Choose ~25% of students to make requests
                for student in random.sample(all_students, int(len(all_students) * 0.25)):
                    doc_type = random.choice(doc_types)
                    
                    # Status: 30% pending, 20% processing, 40% ready, 10% rejected
                    r = random.random()
                    if r < 0.30:
                        status = DocumentRequest.STATUS_PENDING
                        admin_comment = ""
                        processed_date = None
                    elif r < 0.50:
                        status = DocumentRequest.STATUS_PROCESSING
                        admin_comment = "Votre demande est en cours de traitement par le service administratif."
                        processed_date = None
                    elif r < 0.90:
                        status = DocumentRequest.STATUS_READY
                        admin_comment = "Votre document a été édité et est disponible au guichet du secrétariat."
                        processed_date = timezone.now() - datetime.timedelta(days=random.randint(1, 5))
                    else:
                        status = DocumentRequest.STATUS_REJECTED
                        admin_comment = "Demande refusée. Vous devez régulariser votre dossier administratif (photo manquante)."
                        processed_date = timezone.now() - datetime.timedelta(days=random.randint(1, 5))

                    DocumentRequest.objects.create(
                        etudiant=student,
                        document_type=doc_type,
                        comments="Demande urgente pour démarches administratives.",
                        status=status,
                        admin_comment=admin_comment,
                        processed_date=processed_date
                    )
                    doc_request_count += 1

                self.stdout.write(f"Seeded {doc_request_count} student document requests.")

                # 9. Seed Notifications
                self.stdout.write("Seeding user notifications...")
                # Add notifications for teachers
                for teacher in [othman, prof]:
                    Notification.objects.create(
                        user=teacher,
                        title="Nouvelles demandes de justification",
                        message="Vous avez de nouvelles justifications d'absence en attente de validation.",
                        level=Notification.LEVEL_WARNING,
                        link="/justifications/"
                    )
                    Notification.objects.create(
                        user=teacher,
                        title="Planification des examens",
                        message="L'administration a publié le calendrier des examens finaux.",
                        level=Notification.LEVEL_INFO,
                        link="/schedule/"
                    )

                # Add notifications for students with portal logins
                for student in all_students:
                    if student.user:
                        # General welcome
                        Notification.objects.create(
                            user=student.user,
                            title="Bienvenue sur AttendX",
                            message=f"Bonjour {student.nom}, votre compte étudiant a été activé avec succès.",
                            level=Notification.LEVEL_SUCCESS,
                            link="/dashboard/"
                        )
                        # Specific notification if they have any ready document request
                        ready_requests = student.document_requests.filter(status=DocumentRequest.STATUS_READY)
                        if ready_requests.exists():
                            Notification.objects.create(
                                user=student.user,
                                title="Document disponible",
                                message=f"Votre document '{ready_requests.first().document_type}' est prêt au secrétariat.",
                                level=Notification.LEVEL_SUCCESS,
                                link="/documents/"
                            )

                self.stdout.write("Seeding completed successfully!")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error during seeding: {str(e)}"))
            raise e
