#!/usr/bin/env python
"""
Utility script to help add translation tags to templates
This script shows which strings should be wrapped with {% trans %} tags
"""

import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / 'appel' / 'templates'

# Common patterns to search for translations (these should be wrapped with {% trans %})
PATTERNS_TO_TRANSLATE = [
    # Navigation text
    r'Déconnexion',
    r'Connexion',
    r'Mon espace',
    r'Rapports',
    
    # Buttons
    r'Créer la classe',
    r'Se connecter',
    r'Créer un nouveau compte',
    r'Approuver',
    r'Rejeter',
    
    # Labels and headings
    r'Classes',
    r'Étudiants',
    r'Présences',
    r'Absences',
    r'Date',
    r'Salle',
    r'Motif',
    r'Explication',
]

def find_translatable_strings():
    """Find all template files and list translatable strings"""
    print("=" * 80)
    print("TEMPLATE TRANSLATION GUIDE")
    print("=" * 80)
    
    for html_file in TEMPLATES_DIR.glob('*.html'):
        if html_file.name == 'base.html':
            continue  # base.html is already updated
            
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        has_i18n = '{% load i18n %}' in content
        
        print(f"\n📄 {html_file.name}")
        print("-" * 80)
        
        if not has_i18n:
            print("  ⚠️  Missing: {% load i18n %}")
            print(f"  → Add at the top: {{% load i18n %}}")
        else:
            print("  ✓ Has {% load i18n %}")
        
        # Find text that should be translated
        translations_found = []
        for pattern in PATTERNS_TO_TRANSLATE:
            if re.search(pattern, content):
                translations_found.append(pattern)
        
        if translations_found:
            print(f"  Found {len(translations_found)} translatable strings")
            for trans in translations_found[:5]:  # Show first 5
                print(f"    - {trans}")
            if len(translations_found) > 5:
                print(f"    ... and {len(translations_found) - 5} more")

def show_translation_instructions():
    """Show instructions for adding translations"""
    print("\n\n" + "=" * 80)
    print("HOW TO ADD TRANSLATIONS")
    print("=" * 80)
    
    instructions = """
1. In each template, add at the top:
   {% load i18n %}

2. Wrap translatable strings with {% trans %} tags:
   BEFORE: <h1>Bienvenue</h1>
   AFTER:  <h1>{% trans "Welcome" %}</h1>

3. For longer text blocks, use {% blocktrans %}:
   BEFORE: <p>This is a long description</p>
   AFTER:  <p>{% blocktrans %}This is a long description{% endblocktrans %}</p>

4. Update translation files in locale/*/LC_MESSAGES/django.po:
   msgid "Welcome"
   msgstr "Translation here"

5. Recompile translations:
   python compile_translations.py

6. Test language switching:
   Visit /en/, /fr/, or /ar/ in the URL
"""
    
    print(instructions)

if __name__ == '__main__':
    find_translatable_strings()
    show_translation_instructions()
