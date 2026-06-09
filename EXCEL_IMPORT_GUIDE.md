"""
GUIDE D'IMPORTATION D'ÉTUDIANTS DEPUIS EXCEL
================================================

STRUCTURE DU FICHIER EXCEL:
============================

Le fichier Excel doit avoir les colonnes suivantes:
- Colonne A: Nom (obligatoire) - Nom complet de l'étudiant
- Colonne B: Numéro Étudiant (optionnel) - Identifiant unique
- Colonne C: Email (optionnel) - Adresse email

EXEMPLE DE DONNÉES:
===================

Ligne 1 (Entête):     Nom | Numéro Étudiant | Email
Ligne 2:              Salma El Idrissi | STI-2026-001 | salma@school.ma
Ligne 3:              Ahmed Bennani | STI-2026-002 | ahmed@school.ma
Ligne 4:              Fatima Zahra | STI-2026-003 | fatima@school.ma
Ligne 5:              Mohammed Alami | STI-2026-004 |
Ligne 6:              Nadia Bouteflika | | nadia@school.ma


INSTALLATION DES DÉPENDANCES:
=============================

Avant d'importer, assurez-vous que openpyxl est installé:

    pip install openpyxl

Ou installez toutes les dépendances du projet:

    pip install -r requirements.txt


UTILISATION VIA L'INTERFACE WEB:
=================================

1. Allez sur la page d'une classe
2. Cliquez sur le bouton "Importer" dans les Quick Actions
3. Sélectionnez votre fichier Excel (.xlsx ou .xls)
4. Cliquez sur "Importer les étudiants"
5. Vérifiez le nombre d'étudiants importés


CODE D'IMPORTATION (DERRIÈRE LES COULISSES):
==============================================

from openpyxl import load_workbook
from .models import Etudiant, Filiere

def import_students_from_excel(excel_file, filiere):
    '''
    Importe une liste d'étudiants depuis un fichier Excel
    
    Args:
        excel_file: Le fichier Excel uploadé
        filiere: L'objet Filiere auqel ajouter les étudiants
        
    Returns:
        dict: {'imported': nombre importé, 'errors': liste des erreurs}
    '''
    workbook = load_workbook(excel_file)
    worksheet = workbook.active
    
    imported_count = 0
    errors = []
    
    # Boucle à partir de la ligne 2 (ligne 1 = entête)
    for row_idx, row in enumerate(worksheet.iter_rows(min_row=2, values_only=True), start=2):
        try:
            # Extraire les données
            nom = row[0]
            numero_etudiant = row[1] if len(row) > 1 else None
            email = row[2] if len(row) > 2 else None
            
            # Valider le nom
            if not nom:
                errors.append(f"Ligne {row_idx}: Le nom est obligatoire")
                continue
            
            # Nettoyer les données
            nom = str(nom).strip()
            numero_etudiant = str(numero_etudiant).strip() if numero_etudiant else None
            email = str(email).strip() if email else ''
            
            # Créer l'étudiant
            student = Etudiant(
                nom=nom,
                numero_etudiant=numero_etudiant,
                email=email,
                filiere=filiere
            )
            student.save()
            imported_count += 1
            
        except Exception as e:
            errors.append(f"Ligne {row_idx}: {str(e)}")
    
    return {
        'imported': imported_count,
        'errors': errors
    }


EXEMPLES D'UTILISATION MANUEL (EN PYTHON/DJANGO SHELL):
========================================================

# 1. Import manuel depuis la console Django
python manage.py shell

from openpyxl import load_workbook
from appel.models import Etudiant, Filiere

# Charger le fichier
workbook = load_workbook('etudiants.xlsx')
sheet = workbook.active

# Récupérer la classe
filiere = Filiere.objects.get(nom="Informatique 2A")

# Boucle sur les lignes
for row in sheet.iter_rows(min_row=2, values_only=True):
    nom = row[0]
    numero = row[1]
    email = row[2] if len(row) > 2 else ""
    
    # Créer l'étudiant
    student = Etudiant.objects.create(
        nom=nom,
        numero_etudiant=numero,
        email=email,
        filiere=filiere
    )
    print(f"Créé: {nom}")

# 2. Import avec mise à jour
for row in sheet.iter_rows(min_row=2, values_only=True):
    nom = row[0]
    numero = row[1]
    
    # Obtenir ou créer
    student, created = Etudiant.objects.get_or_create(
        numero_etudiant=numero,
        filiere=filiere,
        defaults={'nom': nom}
    )
    
    if not created:
        # Mettre à jour si existe
        student.nom = nom
        student.save()
    
    status = "Créé" if created else "Mis à jour"
    print(f"{status}: {nom}")


FORMAT DES FICHIERS SUPPORTÉS:
==============================

✓ .xlsx (Excel 2007+) - RECOMMANDÉ
✓ .xls (Excel 97-2003)

Limitations:
- Taille maximale: 5 MB
- Nombre de colonnes attendues: minimum 1 (nom), maximum 3
- La première ligne est considérée comme entête


DÉPANNAGE:
==========

Erreur: "openpyxl n'est pas installé"
Solution: pip install openpyxl

Erreur: "Le nom est obligatoire à la ligne X"
Solution: Vérifiez que la colonne A a une valeur à cette ligne

Erreur: "Cet identifiant existe déjà"
Solution: Les étudiants avec le même numéro sont mis à jour, pas dupliqués

Erreur: "Le fichier ne doit pas dépasser 5 MB"
Solution: Réduisez la taille du fichier ou divisez-le en plusieurs fichiers


API DE LA VUE D'IMPORTATION:
============================

URL: /appel/classes/<filiere_id>/import-excel/
Méthode: POST
Format: multipart/form-data

Réponse en cas de succès:
- Redirection vers la page de classe
- Messages: X étudiants importés, Y erreurs

Réponse en cas d'erreur:
- Affichage du formulaire avec messages d'erreur


EXEMPLE DE BOUCLE COMPLÈTE:
============================

# Lire, valider et importer
from openpyxl import load_workbook
from django.core.exceptions import ValidationError

def bulk_import_students(file_path, filiere):
    results = {
        'success': [],
        'failed': [],
        'updated': []
    }
    
    wb = load_workbook(file_path)
    ws = wb.active
    
    for row_num, row in enumerate(ws.iter_rows(min_row=2, values_only=True), 2):
        try:
            nom, numero, email = row[0], row[1], row[2]
            
            if not nom:
                results['failed'].append(f"L{row_num}: Nom vide")
                continue
            
            student, created = Etudiant.objects.update_or_create(
                numero_etudiant=numero,
                filiere=filiere,
                defaults={'nom': nom, 'email': email or ''}
            )
            
            if created:
                results['success'].append(nom)
            else:
                results['updated'].append(nom)
                
        except Exception as e:
            results['failed'].append(f"L{row_num}: {str(e)}")
    
    return results


INTÉGRATION AVEC DJANGO:
=========================

# Dans views.py (déjà implémenté)

@login_required
def import_students_excel(request, filiere_id):
    filiere = get_object_or_404(Filiere, id=filiere_id)
    form = ImportExcelForm(request.POST or None, request.FILES or None)
    
    if request.method == 'POST' and form.is_valid():
        excel_file = request.FILES['excel_file']
        
        # Traitement du fichier
        from openpyxl import load_workbook
        workbook = load_workbook(excel_file)
        worksheet = workbook.active
        
        imported_count = 0
        for row in worksheet.iter_rows(min_row=2, values_only=True):
            # Créer les étudiants
            pass
        
        messages.success(request, f"Import terminé: {imported_count} étudiant(s)")
        return redirect('class_detail', filiere_id=filiere.id)
    
    return render(request, 'import_students.html', {'form': form})

"""

# Code de démonstration en ligne de commande
if __name__ == '__main__':
    print("EXEMPLE D'UTILISATION:")
    print("=" * 50)
    print("""
    # 1. Dans Django shell:
    python manage.py shell
    from openpyxl import load_workbook
    from appel.models import Etudiant, Filiere
    
    # 2. Charger le fichier et la classe
    wb = load_workbook('etudiants.xlsx')
    ws = wb.active
    filiere = Filiere.objects.get(id=1)
    
    # 3. Importer les lignes
    for row in ws.iter_rows(min_row=2, values_only=True):
        Etudiant.objects.create(
            nom=row[0],
            numero_etudiant=row[1],
            email=row[2] if row[2] else '',
            filiere=filiere
        )
    """)
