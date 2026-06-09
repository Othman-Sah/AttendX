from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('logo/', views.logo_file, name='logo_file'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('classes/import-excel/', views.import_classes_excel, name='import_classes_excel'),
    path('profile/', views.user_profile, name='user_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('student/justify/<int:presence_id>/', views.justify_absence, name='justify_absence'),
    path('login/', views.login_view, name='login'),
    path('justifications/', views.manage_justifications, name='manage_justifications'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('select-filiere/', views.select_filiere, name='select_filiere'),
    path('classes/<int:filiere_id>/', views.class_detail, name='class_detail'),
    path('classes/<int:filiere_id>/import-excel/', views.import_students_excel, name='import_students_excel'),
    path('mark-attendance/<int:filiere_id>/', views.mark_attendance, name='mark_attendance'),
    path('select-filiere/<int:filiere_id>/save/', views.save_attendance, name='save_attendance'),
    path('filiere/<int:filiere_id>/rapport-mensuel/', views.generate_monthly_pdf, name='generate_monthly_report'),
    path('rapport-mensuel/', views.monthly_report, name='monthly_report'),
    path('general-information/', views.general_information, name='general_information'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('submitted-documents/', views.submitted_documents, name='submitted_documents'),
    path('manage-documents/', views.manage_documents, name='manage_documents'),
    path('academic-tracking/', views.academic_tracking, name='academic_tracking'),
    path('academic-grades/', views.academic_grades, name='academic_grades'),
    path('absences-classes/', views.absences_classes, name='absences_classes'),
    path('absences-tests/', views.absences_tests, name='absences_tests'),
    path('absences-exams/', views.absences_exams, name='absences_exams'),
    path('cheating/', views.cheating, name='cheating'),
    path('sent-sms/', views.sent_sms, name='sent_sms'),
    # ── Analytics JSON endpoint ────────────────────────────────────────────
    path('analytics/data/', views.analytics_data, name='analytics_data'),
    # ── QR code attendance ─────────────────────────────────────────────────
    path('classes/<int:filiere_id>/qr/', views.qr_session, name='qr_session'),
    path('scan/<uuid:token>/', views.qr_scan, name='qr_scan'),
]
