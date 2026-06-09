#!/usr/bin/env python
"""
Custom message extraction script for Django templates using polib
This replaces the system-dependent makemessages command
"""
import os
import re
import polib
from pathlib import Path

# Django settings setup
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_presence.settings')
django.setup()

from django.conf import settings

BASE_DIR = Path(django.conf.settings.BASE_DIR)
TEMPLATES_DIR = BASE_DIR / 'appel' / 'templates'
LOCALE_DIR = BASE_DIR / 'locale'

def extract_strings_from_template(filepath):
    """Extract translatable strings from a template file"""
    strings = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find {% trans "..." %} and {% trans '...' %}
    trans_patterns = [
        r"{%\s*trans\s+['\"]([^'\"]+)['\"]\s*%}",
        r"{{.*?LANGUAGE_CODE.*?}}",
        r"{%\s*blocktrans\s*%}(.*?){%\s*endblocktrans\s*%}",
    ]
    
    # Also extract common text patterns that should be translated
    # Look for text in buttons, headers, etc.
    text_patterns = [
        r'<h[1-6][^>]*>([^<]+)</h[1-6]>',  # Headers
        r'<button[^>]*>([^<]+)</button>',   # Buttons
        r'<a[^>]*>([^<]+)</a>',             # Links (partial)
        r'type="submit"[^>]*value="([^"]+)"',  # Submit buttons
        r'<label[^>]*>([^<]+)</label>',     # Labels
    ]
    
    for pattern in trans_patterns:
        matches = re.finditer(pattern, content, re.DOTALL)
        for match in matches:
            text = match.group(1).strip()
            if text and len(text) > 0:
                strings.append(text)
    
    return strings

def update_po_files():
    """Update .po files with extracted strings"""
    templates = list(TEMPLATES_DIR.glob('*.html'))
    print(f"Scanning {len(templates)} template files...")
    
    # Extract all strings
    all_strings = set()
    for template_path in templates:
        strings = extract_strings_from_template(template_path)
        all_strings.update(strings)
        if strings:
            print(f"  {template_path.name}: {len(strings)} strings")
    
    print(f"\nTotal unique strings found: {len(all_strings)}")
    
    # Update .po files for each language
    languages = ['en', 'fr', 'ar']
    
    for lang in languages:
        po_path = LOCALE_DIR / lang / 'LC_MESSAGES' / 'django.po'
        
        if po_path.exists():
            print(f"\nUpdating {lang}/LC_MESSAGES/django.po...")
            po = polib.pofile(str(po_path))
            
            # Add new entries
            new_count = 0
            for string in all_strings:
                # Check if entry already exists
                entry = po.find(string)
                if not entry:
                    entry = polib.POEntry(
                        msgid=string,
                        msgstr="",
                        comment="Extracted from templates"
                    )
                    po.append(entry)
                    new_count += 1
            
            # Save updated .po file
            po.save(str(po_path))
            print(f"  Added {new_count} new entries")
        else:
            print(f"  {po_path} not found!")

if __name__ == '__main__':
    update_po_files()
    print("\n✓ Message extraction complete!")
