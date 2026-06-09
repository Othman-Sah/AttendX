#!/usr/bin/env python
"""
Compile and update translation files with comprehensive strings
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_presence.settings')
django.setup()

import polib
from pathlib import Path

BASE_DIR = Path(django.conf.settings.BASE_DIR)
LOCALE_DIR = BASE_DIR / 'locale'

# Comprehensive list of strings from templates
COMMON_STRINGS = {
    'en': {
        # Headers & Navigation
        'Teacher Dashboard': 'Teacher Dashboard',
        'Teacher Studio': 'Teacher Studio',
        'Student Area': 'Student Area',
        'My Profile': 'My Profile',
        'Logout': 'Logout',
        'Change Password': 'Change Password',
        'Create Account': 'Create Account',
        'Create Your Teacher Account': 'Create Your Teacher Account',
        'New Space': 'New Space',
        'New Account': 'New Account',
        'Sign up to add classes, manage students and track attendance in your personal dashboard.': 'Sign up to add classes, manage students and track attendance in your personal dashboard.',
        'Choose a username and password to get started.': 'Choose a username and password to get started.',
        'Registration': 'Registration',
        
        # Classes and Students
        'Classes': 'Classes',
        'Students': 'Students',
        'Active Groups': 'Active Groups',
        'Total Enrolled': 'Total Enrolled',
        'Calls': 'Calls',
        "Today's": "Today's",
        'Rate': 'Rate',
        'Present': 'Present',
        'Absent': 'Absent',
        'Unjustified': 'Unjustified',
        'Create Class': 'Create Class',
        'Add a new group to manage': 'Add a new group to manage',
        'Your Classes': 'Your Classes',
        'Access complete management': 'Access complete management',
        'Active Groups': 'Active Groups',
        'Total Enrolled': 'Total Enrolled',
        
        # Buttons
        'Create': 'Create',
        'Save': 'Save',
        'Submit': 'Submit',
        'Cancel': 'Cancel',
        'Delete': 'Delete',
        'Edit': 'Edit',
        'Open': 'Open',
        'Download': 'Download',
        'Login': 'Login',
        'Sign Up': 'Sign Up',
        'Approve': 'Approve',
        'Reject': 'Reject',
        'Refresh': 'Refresh',
        
        # Status Messages
        'Login successful': 'Login successful',
        'Logout successful': 'Logout successful',
        'Password changed successfully': 'Password changed successfully',
        'Class created successfully': 'Class created successfully',
        'Error on page load': 'Error on page load',
        'Presence': 'Presence',
        'Absence': 'Absence',
        'Justification Pending': 'Justification Pending',
        'Justification Approved': 'Justification Approved',
        'Justification Rejected': 'Justification Rejected',
        
        # Quick Actions
        'Quick Actions': 'Quick Actions',
        'Access main functions': 'Access main functions',
        'Reports & Exports': 'Reports & Exports',
        'Generate monthly documents': 'Generate monthly documents',
        'Monthly Report': 'Monthly Report',
        'Justifications': 'Justifications',
        
        # Forms
        'Username': 'Username',
        'Password': 'Password',
        'Email': 'Email',
        'First Name': 'First Name',
        'Last Name': 'Last Name',
        'Room': 'Room',
        'Select a class': 'Select a class',
        'No classes available': 'No classes available',
        'No classes for now': 'No classes for now',
        'Create your first class to get started': 'Create your first class to get started',
        
        # Sidebar Options
        'General Information': 'General Information',
        'Calendar': 'Calendar',
        'Submitted Documents': 'Submitted Documents',
        'Semester 2': 'Semester 2',
        'Academic Tracking': 'Academic Tracking',
        'Academic Grades S2': 'Academic Grades S2',
        'Attendance': 'Attendance',
        'Absences in Classes S2': 'Absences in Classes S2',
        'Absences in Tests S2': 'Absences in Tests S2',
        'Absences in Exams S2': 'Absences in Exams S2',
        'Incidents': 'Incidents',
        'Cheating S2': 'Cheating S2',
        'Communication': 'Communication',
        'Sent SMS S2': 'Sent SMS S2',
    },
    'fr': {
        'Teacher Dashboard': 'Tableau de Bord Enseignant',
        'Teacher Studio': 'Studio Enseignant',
        'Student Area': 'Espace Étudiant',
        'My Profile': 'Mon Profil',
        'Logout': 'Déconnexion',
        'Change Password': 'Changer de mot de passe',
        'Create Account': 'Créer un compte',
        'Create Your Teacher Account': 'Créez votre compte enseignant',
        'New Space': 'Nouvel Espace',
        'New Account': 'Nouveau Compte',
        'Sign up to add classes, manage students and track attendance in your personal dashboard.': 'Inscrivez-vous pour ajouter des classes, gérer les étudiants et suivre les présences dans votre tableau de bord personnel.',
        'Choose a username and password to get started.': 'Choisissez un identifiant et un mot de passe pour commencer.',
        'Registration': 'Inscription',
        
        'Classes': 'Classes',
        'Students': 'Étudiants',
        'Active Groups': 'Groupes Actifs',
        'Total Enrolled': 'Total Inscrit',
        'Calls': 'Appels',
        "Today's": "D'Aujourd'hui",
        'Rate': 'Taux',
        'Present': 'Présent',
        'Absent': 'Absent',
        'Unjustified': 'Injustifié',
        'Create Class': 'Créer une Classe',
        'Add a new group to manage': 'Ajoutez un nouveau groupe à gérer',
        'Your Classes': 'Vos Classes',
        'Access complete management': 'Accédez à la gestion complète',
        
        'Create': 'Créer',
        'Save': 'Enregistrer',
        'Submit': 'Soumettre',
        'Cancel': 'Annuler',
        'Delete': 'Supprimer',
        'Edit': 'Modifier',
        'Open': 'Ouvrir',
        'Download': 'Télécharger',
        'Login': 'Connexion',
        'Sign Up': 'S\'inscrire',
        'Approve': 'Approuver',
        'Reject': 'Rejeter',
        'Refresh': 'Rafraîchir',
        
        'Login successful': 'Connexion réussie',
        'Logout successful': 'Déconnexion réussie',
        'Password changed successfully': 'Mot de passe changé avec succès',
        'Class created successfully': 'Classe créée avec succès',
        'Error on page load': 'Erreur lors du chargement de la page',
        'Presence': 'Présence',
        'Absence': 'Absence',
        'Justification Pending': 'Justification En Attente',
        'Justification Approved': 'Justification Approuvée',
        'Justification Rejected': 'Justification Rejetée',
        
        'Quick Actions': 'Actions Rapides',
        'Access main functions': 'Accédez aux fonctions principales',
        'Reports & Exports': 'Rapports & Exports',
        'Generate monthly documents': 'Générez les documents mensuels',
        'Monthly Report': 'Rapport Mensuel',
        'Justifications': 'Justifications',
        
        'Username': 'Nom d\'utilisateur',
        'Password': 'Mot de passe',
        'Email': 'Email',
        'First Name': 'Prénom',
        'Last Name': 'Nom',
        'Room': 'Salle',
        'Select a class': 'Sélectionnez une classe',
        'No classes available': 'Aucune classe disponible',
        'No classes for now': 'Aucune classe pour le moment',
        'Create your first class to get started': 'Créez votre première classe pour commencer',
        
        # Sidebar Options
        'General Information': 'Informations Générales',
        'Calendar': 'Calendrier',
        'Submitted Documents': 'Documents Soumis',
        'Semester 2': 'Semestre 2',
        'Academic Tracking': 'Suivi Académique',
        'Academic Grades S2': 'Notes Académiques S2',
        'Attendance': 'Présences',
        'Absences in Classes S2': 'Absences en Cours S2',
        'Absences in Tests S2': 'Absences aux Contrôles S2',
        'Absences in Exams S2': 'Absences aux Examens S2',
        'Incidents': 'Incidents',
        'Cheating S2': 'Triche S2',
        'Communication': 'Communication',
        'Sent SMS S2': 'SMS Envoyés S2',
    },
    'ar': {
        'Teacher Dashboard': 'لوحة تحكم المعلم',
        'Teacher Studio': 'استوديو المعلم',
        'Student Area': 'منطقة الطالب',
        'My Profile': 'ملفي الشخصي',
        'Logout': 'تسجيل الخروج',
        'Change Password': 'تغيير كلمة المرور',
        'Create Account': 'إنشاء حساب',
        'Create Your Teacher Account': 'أنشئ حساب المعلم الخاص بك',
        'New Space': 'مساحة جديدة',
        'New Account': 'حساب جديد',
        'Sign up to add classes, manage students and track attendance in your personal dashboard.': 'قم بالتسجيل لإضافة فصول وإدارة الطلاب وتتبع الحضور في لوحة التحكم الشخصية الخاصة بك.',
        'Choose a username and password to get started.': 'اختر اسم المستخدم وكلمة المرور للبدء.',
        'Registration': 'التسجيل',
        
        'Classes': 'الفصول',
        'Students': 'الطلاب',
        'Active Groups': 'المجموعات النشطة',
        'Total Enrolled': 'المجموع المسجل',
        'Calls': 'الاستدعاءات',
        "Today's": 'اليوم',
        'Rate': 'معدل',
        'Present': 'حاضر',
        'Absent': 'غائب',
        'Unjustified': 'بدون عذر',
        'Create Class': 'إنشاء فصل',
        'Add a new group to manage': 'أضف مجموعة جديدة لإدارتها',
        'Your Classes': 'فصولك',
        'Access complete management': 'الوصول إلى الإدارة الكاملة',
        
        'Create': 'إنشاء',
        'Save': 'حفظ',
        'Submit': 'إرسال',
        'Cancel': 'إلغاء',
        'Delete': 'حذف',
        'Edit': 'تحرير',
        'Open': 'فتح',
        'Download': 'تحميل',
        'Login': 'دخول',
        'Sign Up': 'اشتراك',
        'Approve': 'موافقة',
        'Reject': 'رفض',
        'Refresh': 'تحديث',
        
        'Login successful': 'تم تسجيل الدخول بنجاح',
        'Logout successful': 'تم تسجيل الخروج بنجاح',
        'Password changed successfully': 'تم تغيير كلمة المرور بنجاح',
        'Class created successfully': 'تم إنشاء الفصل بنجاح',
        'Error on page load': 'خطأ عند تحميل الصفحة',
        'Presence': 'الحضور',
        'Absence': 'الغياب',
        'Justification Pending': 'التبرير قيد الانتظار',
        'Justification Approved': 'تم الموافقة على التبرير',
        'Justification Rejected': 'تم رفض التبرير',
        
        'Quick Actions': 'إجراءات سريعة',
        'Access main functions': 'الوصول إلى الوظائف الرئيسية',
        'Reports & Exports': 'التقارير والتصدير',
        'Generate monthly documents': 'إنشاء المستندات الشهرية',
        'Monthly Report': 'التقرير الشهري',
        'Justifications': 'التبريرات',
        
        'Username': 'اسم المستخدم',
        'Password': 'كلمة المرور',
        'Email': 'البريد الإلكتروني',
        'First Name': 'الاسم الأول',
        'Last Name': 'اسم العائلة',
        'Room': 'الغرفة',
        'Select a class': 'حدد فصلاً',
        'No classes available': 'لا توجد فصول متاحة',
        'No classes for now': 'لا توجد فصول في الوقت الحالي',
        'Create your first class to get started': 'أنشئ فصلك الأول للبدء',
        
        # Sidebar Options
        'General Information': 'معلومات عامة',
        'Calendar': 'التقويم',
        'Submitted Documents': 'المستندات المقدمة',
        'Semester 2': 'الفصل الدراسي الثاني',
        'Academic Tracking': 'المتابعة الأكاديمية',
        'Academic Grades S2': 'الدرجات الأكاديمية (الفصل الثاني)',
        'Attendance': 'الحضور',
        'Absences in Classes S2': 'الغياب في الفصول (الفصل الثاني)',
        'Absences in Tests S2': 'الغياب في الاختبارات (الفصل الثاني)',
        'Absences in Exams S2': 'الغياب في الامتحانات (الفصل الثاني)',
        'Incidents': 'أحداث',
        'Cheating S2': 'حالات الغش (الفصل الثاني)',
        'Communication': 'التواصل',
        'Sent SMS S2': 'الرسائل النصية المرسلة (الفصل الثاني)',
    }
}

def add_strings_to_po_files():
    """Add all strings to .po files"""
    for lang, strings_dict in COMMON_STRINGS.items():
        po_path = LOCALE_DIR / lang / 'LC_MESSAGES' / 'django.po'
        
        if not po_path.exists():
            print(f"⚠ {po_path} not found!")
            continue
            
        po = polib.pofile(str(po_path))
        added_count = 0
        
        for msgid, msgstr in strings_dict.items():
            entry = po.find(msgid)
            if not entry:
                entry = polib.POEntry(msgid=msgid, msgstr=msgstr if lang != 'en' else msgid)
                po.append(entry)
                added_count += 1
            elif lang != 'en' and not entry.msgstr:
                # Update empty translation
                entry.msgstr = msgstr
                added_count += 1
        
        po.save(str(po_path))
        print(f"✓ {lang}: Added/Updated {added_count} entries")


def compile_translations():
    """Compile .po files to .mo files"""
    languages = ['en', 'fr', 'ar']
    compiled_count = 0
    
    for lang in languages:
        po_path = LOCALE_DIR / lang / 'LC_MESSAGES' / 'django.po'
        mo_path = LOCALE_DIR / lang / 'LC_MESSAGES' / 'django.mo'
        
        if po_path.exists():
            po = polib.pofile(str(po_path))
            po.save_as_mofile(str(mo_path))
            compiled_count += 1
            print(f"✓ Compiled: {lang}/LC_MESSAGES/django.mo")
    
    return compiled_count

if __name__ == '__main__':
    print("Adding translation strings...")
    add_strings_to_po_files()
    print("\nCompiling translation files...")
    count = compile_translations()
    print(f"\n✓ Successfully compiled {count} translation files!")
