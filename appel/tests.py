from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from datetime import timedelta, time
from django.utils.timezone import now

from django.core.files.uploadedfile import SimpleUploadedFile

from .defaults import DEFAULT_TEACHER_PASSWORD, DEFAULT_TEACHER_USERNAME
from .forms import ClassScheduleForm, ImportExcelForm
from .models import AbsenceJustification, ClassSchedule, Etudiant, Filiere, Presence


class ClassroomFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='prof', password='securepass123')
        self.admin_user = User.objects.create_user(username='admin-test', password='securepass123', is_staff=True)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_logged_user_can_create_class(self):
        self.client.login(username='admin-test', password='securepass123')
        teacher = User.objects.create_user(username='teacher-create', password='teacherpass123')
        response = self.client.post(
            reverse('dashboard'),
            {
                'nom': 'Informatique 1',
                'salle': 'B12',
                'description': 'Classe de premiere annee',
                'teacher': teacher.id,
                'class_date': '2026-05-06',
                'day_of_week': '',
                'start_time': '08:30',
                'end_time': '10:30',
                'subject': 'Python',
                'session_type': ClassSchedule.SESSION_EXAM,
                'room': 'B12',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Filiere.objects.filter(nom='Informatique 1').exists())
        filiere = Filiere.objects.get(nom='Informatique 1')
        self.assertEqual(filiere.teacher, teacher)
        schedule = ClassSchedule.objects.get(filiere=filiere, subject='Python')
        self.assertEqual(str(schedule.class_date), '2026-05-06')
        self.assertEqual(schedule.start_time.strftime('%H:%M'), '08:30')
        self.assertEqual(schedule.session_type, ClassSchedule.SESSION_EXAM)

    def test_login_page_creates_default_teacher_account(self):
        User.objects.filter(username='prof').delete()
        User.objects.filter(username=DEFAULT_TEACHER_USERNAME).delete()

        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username=DEFAULT_TEACHER_USERNAME, is_staff=False).exists())
        self.assertTrue(self.client.login(username=DEFAULT_TEACHER_USERNAME, password=DEFAULT_TEACHER_PASSWORD))
        teacher = User.objects.get(username=DEFAULT_TEACHER_USERNAME)
        self.assertEqual(teacher.first_name, 'Othman')

    def test_logged_user_can_add_student_to_class(self):
        self.client.login(username='admin-test', password='securepass123')
        filiere = Filiere.objects.create(nom='Maths')
        response = self.client.post(
            reverse('class_detail', args=[filiere.id]),
            {
                'action': 'add_student',
                'nom': 'Aya Bennani',
                'numero_etudiant': 'MAT-001',
                'email': 'aya@example.com',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Etudiant.objects.filter(nom='Aya Bennani', filiere=filiere).exists())

    def test_attendance_updates_student_totals(self):
        self.client.login(username='prof', password='securepass123')
        filiere = Filiere.objects.create(nom='Sciences')
        ClassSchedule.objects.create(
            filiere=filiere,
            day_of_week='Monday',
            start_time=time(8, 0),
            end_time=time(10, 0),
            subject='Science',
            professor='prof',
        )
        student = Etudiant.objects.create(nom='Youssef', filiere=filiere)

        response = self.client.post(reverse('save_attendance', args=[filiere.id]), {f'present_{student.id}': 'on'})

        self.assertEqual(response.status_code, 200)
        student.refresh_from_db()
        self.assertEqual(student.total_presences, 1)
        self.assertEqual(student.total_absences, 0)
        self.assertTrue(Presence.objects.filter(etudiant=student, present=True).exists())

    def test_user_can_create_account_from_signup_page(self):
        filiere = Filiere.objects.create(nom='Student Class')
        student = Etudiant.objects.create(nom='New Student', filiere=filiere, numero_etudiant='STU-001')
        response = self.client.post(
            reverse('signup'),
            {
                'username': 'newstudent',
                'email': 'student@example.com',
                'full_name': 'New Student',
                'filiere': filiere.id,
                'student_number': 'STU-001',
                'password1': 'StrongPass123',
                'password2': 'StrongPass123',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newstudent').exists())
        student.refresh_from_db()
        self.assertIsNotNone(student.user)
        self.assertEqual(student.user.username, 'newstudent')

    def test_student_account_is_created_when_requested(self):
        self.client.login(username='admin-test', password='securepass123')
        filiere = Filiere.objects.create(nom='Gestion')

        response = self.client.post(
            reverse('class_detail', args=[filiere.id]),
            {
                'action': 'add_student',
                'nom': 'Lina',
                'numero_etudiant': 'GST-001',
                'email': 'lina@example.com',
                'create_student_account': 'on',
                'student_username': 'lina.student',
                'student_password': 'studentpass123',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        student = Etudiant.objects.get(numero_etudiant='GST-001')
        self.assertIsNotNone(student.user)
        self.assertEqual(student.user.username, 'lina.student')

    def test_student_is_redirected_to_student_dashboard_after_login(self):
        student_user = User.objects.create_user(username='student1', password='studentpass123')
        filiere = Filiere.objects.create(nom='Reseaux')
        Etudiant.objects.create(nom='Hajar', filiere=filiere, user=student_user)

        response = self.client.post(
            reverse('login'),
            {'username': 'student1', 'password': 'studentpass123'},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('student_dashboard'))

    def test_student_can_submit_absence_justification(self):
        student_user = User.objects.create_user(username='student2', password='studentpass123')
        filiere = Filiere.objects.create(nom='Commerce')
        student = Etudiant.objects.create(nom='Sara', filiere=filiere, user=student_user)
        presence = Presence.objects.create(etudiant=student, present=False)

        self.client.login(username='student2', password='studentpass123')
        response = self.client.post(
            reverse('justify_absence', args=[presence.id]),
            {
                'reason': 'Motif medical',
                'details': 'Consultation chez le medecin',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(AbsenceJustification.objects.filter(presence=presence, reason='Motif medical').exists())

    def test_admin_can_manage_justifications(self):
        # Create a student and an absence with justification
        filiere = Filiere.objects.create(nom='Informatique')
        student_user = User.objects.create_user(username='student_for_justify', password='studentpass')
        student = Etudiant.objects.create(nom='Alice', filiere=filiere, user=student_user)
        presence = Presence.objects.create(etudiant=student, present=False)
        justification = AbsenceJustification.objects.create(
            presence=presence,
            reason='Maladie',
            details='Fièvre',
            status=AbsenceJustification.STATUS_PENDING,
        )

        self.client.login(username='admin-test', password='securepass123')

        response = self.client.post(
            reverse('manage_justifications'),
            {'justification_id': justification.id, 'action': 'approve'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        justification.refresh_from_db()
        self.assertEqual(justification.status, AbsenceJustification.STATUS_APPROVED)

    def test_non_admin_teacher_cannot_manage_justifications(self):
        filiere = Filiere.objects.create(nom='Bio')
        student_user = User.objects.create_user(username='student-no-admin', password='studentpass')
        student = Etudiant.objects.create(nom='Karim', filiere=filiere, user=student_user)
        presence = Presence.objects.create(etudiant=student, present=False)
        justification = AbsenceJustification.objects.create(
            presence=presence,
            reason='Transport',
            details='Bus delay',
            status=AbsenceJustification.STATUS_PENDING,
        )

        self.client.login(username='prof', password='securepass123')
        response = self.client.post(
            reverse('manage_justifications'),
            {'justification_id': justification.id, 'action': 'approve'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        justification.refresh_from_db()
        self.assertEqual(justification.status, AbsenceJustification.STATUS_PENDING)

    def test_student_calendar_is_ordered_by_weekday(self):
        student_user = User.objects.create_user(username='student-calendar', password='studentpass123')
        filiere = Filiere.objects.create(nom='Planning')
        Etudiant.objects.create(nom='Imane', filiere=filiere, user=student_user)

        ClassSchedule.objects.create(
            filiere=filiere,
            day_of_week='Wednesday',
            start_time=time(14, 0),
            end_time=time(16, 0),
            subject='Algorithms',
        )
        ClassSchedule.objects.create(
            filiere=filiere,
            day_of_week='Monday',
            start_time=time(9, 0),
            end_time=time(11, 0),
            subject='Databases',
        )

        self.client.login(username='student-calendar', password='studentpass123')
        response = self.client.get(reverse('calendar'))

        self.assertEqual(response.status_code, 200)
        grouped_days = response.context['calendar_sections'][0]['grouped_days']
        self.assertEqual([day['label'] for day in grouped_days], ['Lundi', 'Mercredi'])

    def test_teacher_calendar_lists_all_classes_with_schedules(self):
        self.client.login(username='prof', password='securepass123')
        filiere_a = Filiere.objects.create(nom='GI 1')
        filiere_b = Filiere.objects.create(nom='GI 2')

        ClassSchedule.objects.create(
            filiere=filiere_a,
            day_of_week='Monday',
            start_time=time(8, 30),
            end_time=time(10, 0),
            subject='Maths',
            professor='prof',
        )
        ClassSchedule.objects.create(
            filiere=filiere_b,
            day_of_week='Tuesday',
            start_time=time(10, 0),
            end_time=time(12, 0),
            subject='Reseaux',
            professor='other-teacher',
        )

        response = self.client.get(reverse('calendar'))

        self.assertEqual(response.status_code, 200)
        section_names = [section['filiere'].nom for section in response.context['calendar_sections'] if section['total_sessions']]
        self.assertEqual(section_names, ['GI 1'])

    def test_teacher_pages_render_with_clean_templates(self):
        self.client.login(username='prof', password='securepass123')
        filiere = Filiere.objects.create(nom='Design UI', salle='A2', teacher=User.objects.get(username='prof'))
        ClassSchedule.objects.create(
            filiere=filiere,
            day_of_week='Monday',
            start_time=time(9, 0),
            end_time=time(11, 0),
            subject='UX',
            professor='prof',
        )
        Etudiant.objects.create(nom='Nadia', filiere=filiere, email='nadia@example.com')

        urls = [
            reverse('calendar'),
            reverse('select_filiere'),
            reverse('class_detail', args=[filiere.id]),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

        self.client.logout()
        self.client.login(username='admin-test', password='securepass123')
        response = self.client.get(reverse('manage_justifications'))
        self.assertEqual(response.status_code, 200)

    def test_teacher_phase_lists_classes_and_attendance(self):
        self.client.login(username='prof', password='securepass123')
        filiere = Filiere.objects.create(nom='GI 3', salle='C14', teacher=User.objects.get(username='prof'))
        present_student = Etudiant.objects.create(nom='Amina', filiere=filiere)
        absent_student = Etudiant.objects.create(nom='Hamza', filiere=filiere)
        ClassSchedule.objects.create(
            filiere=filiere,
            day_of_week='Wednesday',
            start_time=time(8, 0),
            end_time=time(10, 0),
            subject='Algo',
            professor='prof',
        )
        Presence.objects.create(etudiant=present_student, present=True, date=now().date())
        Presence.objects.create(etudiant=absent_student, present=False, date=now().date())

        response = self.client.get(reverse('select_filiere'))

        self.assertEqual(response.status_code, 200)
        page = response.content.decode()
        self.assertIn('GI 3', page)
        self.assertIn('Voir / marquer', page)
        listed_class = response.context['filieres'][0]
        self.assertEqual(listed_class.present_count, 1)
        self.assertEqual(listed_class.absent_count, 1)

    def test_teacher_is_redirected_away_from_admin_pages(self):
        self.client.login(username='prof', password='securepass123')

        for url in [reverse('manage_documents'), reverse('monthly_report'), reverse('general_information')]:
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.request['PATH_INFO'], reverse('calendar'))

    def test_teacher_is_redirected_away_from_profile_and_notifications_pages(self):
        self.client.login(username='prof', password='securepass123')

        for url in [reverse('notifications'), reverse('user_profile'), reverse('update_profile'), reverse('change_password')]:
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.request['PATH_INFO'], reverse('calendar'))

    def test_teacher_cannot_open_other_teachers_class(self):
        self.client.login(username='prof', password='securepass123')
        own_teacher = User.objects.get(username='prof')
        other_teacher = User.objects.create_user(username='other-teacher-account', password='teacherpass123')
        own_class = Filiere.objects.create(nom='Own Class', teacher=own_teacher)
        other_class = Filiere.objects.create(nom='Other Class', teacher=other_teacher)
        ClassSchedule.objects.create(
            filiere=own_class,
            day_of_week='Monday',
            start_time=time(8, 0),
            end_time=time(10, 0),
            subject='Maths',
            professor='prof',
        )
        ClassSchedule.objects.create(
            filiere=other_class,
            day_of_week='Tuesday',
            start_time=time(10, 0),
            end_time=time(12, 0),
            subject='Physics',
            professor='other-teacher',
        )

        allowed_response = self.client.get(reverse('class_detail', args=[own_class.id]))
        denied_response = self.client.get(reverse('class_detail', args=[other_class.id]), follow=True)

        self.assertEqual(allowed_response.status_code, 200)
        self.assertEqual(denied_response.status_code, 200)
        self.assertEqual(denied_response.request['PATH_INFO'], reverse('select_filiere'))

    def test_teacher_layout_only_shows_timetable_and_absence_actions(self):
        self.client.login(username='prof', password='securepass123')
        response = self.client.get(reverse('calendar'))

        self.assertEqual(response.status_code, 200)
        page = response.content.decode()
        self.assertIn('Planning', page)
        self.assertIn('Absences', page)
        self.assertNotIn('Notifications', page)
        self.assertNotIn('Profil', page)

    def test_admin_assigns_teacher_to_class_and_teacher_sees_it(self):
        teacher = User.objects.create_user(username='assigned-teacher', password='teacherpass123')
        self.client.login(username='admin-test', password='securepass123')
        create_response = self.client.post(
            reverse('dashboard'),
            {
                'nom': 'Assigned Class',
                'salle': 'A8',
                'description': 'Classe test',
                'teacher': teacher.id,
            },
            follow=True,
        )

        self.assertEqual(create_response.status_code, 200)
        filiere = Filiere.objects.get(nom='Assigned Class')
        self.assertEqual(filiere.teacher, teacher)

        ClassSchedule.objects.create(
            filiere=filiere,
            day_of_week='Thursday',
            start_time=time(14, 0),
            end_time=time(16, 0),
            subject='Networks',
        )

        self.client.logout()
        self.client.login(username='assigned-teacher', password='teacherpass123')

        calendar_response = self.client.get(reverse('calendar'))
        classes_response = self.client.get(reverse('select_filiere'))

        self.assertEqual(calendar_response.status_code, 200)
        self.assertEqual(classes_response.status_code, 200)
        self.assertIn('Assigned Class', calendar_response.content.decode())
        self.assertIn('Assigned Class', classes_response.content.decode())

    def test_admin_assigned_class_appears_in_othman_timetable(self):
        teacher = User.objects.create_user(username=DEFAULT_TEACHER_USERNAME, password=DEFAULT_TEACHER_PASSWORD)
        self.client.login(username='admin-test', password='securepass123')
        filiere = Filiere.objects.create(nom='Othman Assigned Class', teacher=teacher)
        ClassSchedule.objects.create(
            filiere=filiere,
            day_of_week='Friday',
            start_time=time(9, 0),
            end_time=time(11, 0),
            subject='Programmation',
        )

        self.client.logout()
        self.client.login(username=DEFAULT_TEACHER_USERNAME, password=DEFAULT_TEACHER_PASSWORD)
        response = self.client.get(reverse('calendar'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Othman Assigned Class')
        self.assertContains(response, 'Programmation')

    def test_student_pages_render_with_clean_templates(self):
        student_user = User.objects.create_user(username='student-render', password='studentpass123')
        filiere = Filiere.objects.create(nom='Classe B')
        student = Etudiant.objects.create(nom='Salma', filiere=filiere, user=student_user)
        Presence.objects.create(etudiant=student, present=False)

        self.client.login(username='student-render', password='studentpass123')
        urls = [
            reverse('student_dashboard'),
            reverse('calendar'),
            reverse('absences_classes'),
            reverse('user_profile'),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_admin_class_absences_lists_every_class_with_absences(self):
        class_a = Filiere.objects.create(nom='Admin Absence A')
        class_b = Filiere.objects.create(nom='Admin Absence B')
        student_a = Etudiant.objects.create(nom='Absent A', filiere=class_a)
        student_b = Etudiant.objects.create(nom='Absent B', filiere=class_b)
        Presence.objects.create(etudiant=student_a, present=False, date=now().date())
        Presence.objects.create(etudiant=student_b, present=False, date=now().date())

        self.client.login(username='admin-test', password='securepass123')
        response = self.client.get(reverse('absences_classes'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['admin_mode'])
        self.assertContains(response, 'Admin Absence A')
        self.assertContains(response, 'Admin Absence B')
        self.assertContains(response, 'Absent A')
        self.assertContains(response, 'Absent B')

    def test_excel_import_form_accepts_uppercase_extensions(self):
        form = ImportExcelForm(
            files={'excel_file': SimpleUploadedFile('students.XLSX', b'dummy-data')},
        )

        self.assertTrue(form.is_valid())

    def test_class_schedule_form_uses_date_to_fill_day(self):
        form = ClassScheduleForm(
            data={
                'class_date': '2026-04-27',
                'day_of_week': '',
                'start_time': '08:00',
                'end_time': '10:00',
                'subject': 'Maths',
                'room': 'A1',
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['day_of_week'], 'Monday')

    def test_admin_can_set_class_date_and_time(self):
        teacher = User.objects.create_user(username='planning-teacher', password='teacherpass123')
        filiere = Filiere.objects.create(nom='Planning Class', teacher=teacher)
        self.client.login(username='admin-test', password='securepass123')

        response = self.client.post(
            reverse('class_detail', args=[filiere.id]),
            {
                'action': 'add_schedule',
                'class_date': '2026-05-04',
                'day_of_week': '',
                'start_time': '09:00',
                'end_time': '11:00',
                'subject': 'Programmation',
                'session_type': ClassSchedule.SESSION_EXAM,
                'room': 'B15',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        schedule = ClassSchedule.objects.get(filiere=filiere, subject='Programmation')
        self.assertEqual(str(schedule.class_date), '2026-05-04')
        self.assertEqual(schedule.day_of_week, 'Monday')
        self.assertEqual(schedule.professor, 'planning-teacher')
        self.assertEqual(schedule.session_type, ClassSchedule.SESSION_EXAM)

    def test_student_refresh_attendance_totals_recomputes_counts(self):
        filiere = Filiere.objects.create(nom='Compta')
        student = Etudiant.objects.create(nom='Nadia', filiere=filiere)
        Presence.objects.create(etudiant=student, present=True, date=now().date())
        Presence.objects.create(etudiant=student, present=False, date=now().date() - timedelta(days=1))

        student.refresh_attendance_totals()
        student.refresh_from_db()

        self.assertEqual(student.total_presences, 1)
        self.assertEqual(student.total_absences, 1)
