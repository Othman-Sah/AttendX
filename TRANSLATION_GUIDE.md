# Multi-Language Support Guide

## ✅ **How Language Switching Works**

Your application now supports **3 languages**:
- 🇬🇧 **English** (`/en/...`)
- 🇫🇷 **Français** (`/fr/...`) 
- 🇸🇦 **العربية** (`/ar/...`)

### **Language Selector**
The language dropdown is in the top navbar. Users can switch languages anytime:
1. Click the 🌐 globe icon in the navbar
2. Select their preferred language
3. The entire interface updates

### **How It Works**
- Django's `LocaleMiddleware` detects the language from the URL
- URLs are automatically prefixed with language codes
- When you switch languages, Django changes the session language
- All wrapped strings automatically translate

---

## 📝 **Making Text Translatable**

### **Step 1: Load Translation Tags**
At the top of each template, add:
```django
{% load i18n %}
```

### **Step 2: Wrap Text with Translation Tags**

#### **For short text:**
```django
<!-- BEFORE -->
<button>Se connecter</button>

<!-- AFTER using {% trans %} -->
<button>{% trans "Login" %}</button>
```

#### **For longer text:**
```django
<!-- BEFORE -->
<p>This is a description about the classroom management system.</p>

<!-- AFTER using {% blocktrans %} -->
<p>{% blocktrans %}This is a description about the classroom management system.{% endblocktrans %}</p>
```

#### **For variables:**
```django
<!-- Use simple variables inside trans -->
<p>{% trans "Hello" %} {{ user.name }}</p>

<!-- For complex variables, use blocktrans -->
{% blocktrans with total=count %}
You have {{ total }} messages
{% endblocktrans %}
```

---

## 🌍 **Updating Translation Files**

### **Location of Translation Files**
```
locale/
├── en/LC_MESSAGES/
│   ├── django.po      (Translations to English)
│   └── django.mo      (Compiled - binary format)
├── fr/LC_MESSAGES/
│   ├── django.po      (Translations to French)
│   └── django.mo
└── ar/LC_MESSAGES/
    ├── django.po      (Translations to Arabic)
    └── django.mo
```

### **Format of .po Files**
```
msgid "Login"
msgstr "Se connecter"
```

- `msgid` = Original English text
- `msgstr` = Translated text

### **Example .po Entry**
```
# Comment about the string
msgid "Welcome"
msgstr "Bienvenue"

msgid "Class Name"
msgstr "Nom de la Classe"

msgid "Teacher"
msgstr "Professeur"
```

---

## 🔧 **Working with Translations**

### **1. Add a New Translatable String**

**In your template:**
```django
<h1>{% trans "My Classes" %}</h1>
```

**In `locale/en/LC_MESSAGES/django.po`:**
```
msgid "My Classes"
msgstr "My Classes"
```

**In `locale/fr/LC_MESSAGES/django.po`:**
```
msgid "My Classes"
msgstr "Mes Classes"
```

**In `locale/ar/LC_MESSAGES/django.po`:**
```
msgid "My Classes"
msgstr "فصولي"
```

### **2. Recompile Translations**
After updating .po files, run:
```bash
python compile_translations.py
```

This converts `.po` files to `.mo` (binary) files that Django reads.

### **3. Test the Translation**
1. Start your Django server: `python manage.py runserver`
2. Visit: `http://localhost:8000/en/` (English)
3. Switch to French: `http://localhost:8000/fr/`
4. Switch to Arabic: `http://localhost:8000/ar/`

---

## 📋 **Common Translation Patterns**

### **Navigation Elements**
```django
<a href="{% url 'dashboard' %}">{% trans "Dashboard" %}</a>
<button>{% trans "Logout" %}</button>
```

### **Form Labels**
```django
<label for="name">{% trans "Full Name" %}</label>
<label for="email">{% trans "Email Address" %}</label>
```

### **Error Messages**
```django
{% if form.errors %}
    <p class="error">{% trans "Please correct the errors below." %}</p>
{% endif %}
```

### **Pluralization**
```django
{% blocktrans count counter=students %}
  You have {{ counter }} student
{% plural %}
  You have {{ counter }} students
{% endblocktrans %}
```

---

## 🎯 **Currently Translated Strings**

### **Completed Templates**
- ✅ **login.html** - All text translated
- ✅ **base.html** - Navigation translated
- ⏳ **home.html** - Partial translations
- ⏳ **student_dashboard.html** - Partial translations
- ⏳ **manage_justifications.html** - Partial translations

### **Ready-to-Use Translations**
The following strings are already translated in all 3 languages:
- Navigation: Login, Logout, Dashboard, Profile, etc.
- Admin: Classes, Students, Reports, Justifications
- Buttons: Create, Approve, Reject, Save, Cancel
- Status: Pending, Approved, Rejected, Present, Absent

---

## 🚀 **Quick Reference**

| Action | Command |
|--------|---------|
| View English site | Visit `/en/login/` |
| View French site | Visit `/fr/login/` |
| View Arabic site | Visit `/ar/login/` |
| Add new string | Add `{% trans "..." %}` in template |
| Update translations | Edit `locale/*/LC_MESSAGES/django.po` |
| Compile translations | Run `python compile_translations.py` |
| Check config | Run `python manage.py check` |

---

## ⚙️ **Technical Details**

### **Settings Configuration**
In `gestion_presence/settings.py`:
```python
LANGUAGE_CODE = 'fr'

LANGUAGES = [
    ('en', 'English'),
    ('fr', 'Français'),
    ('ar', 'العربية'),
]

LOCALE_PATHS = [BASE_DIR / 'locale']
```

### **Middleware**
The `LocaleMiddleware` is enabled in MIDDLEWARE:
```python
MIDDLEWARE = [
    'django.middleware.locale.LocaleMiddleware',
    # ... other middleware ...
]
```

### **URL Configuration**
URLs are wrapped with `i18n_patterns()`:
```python
urlpatterns += i18n_patterns(
    path('', include('appel.urls')),
)
```

---

## 💡 **Tips**

1. **Always use English in `msgid`** - msgid should always be the original English text
2. **Keep messages simple** - Shorter strings are easier to translate accurately
3. **Use descriptive comments** - Add comments in .po files for context:
   ```
   # Button to submit the form
   msgid "Submit"
   msgstr "Soumettre"
   ```
4. **Test all languages** - Always verify translations appear correctly
5. **RTL Support** - For Arabic, add `dir="rtl"` to `<html>` tag (already done in base.html)

---

## 🐛 **Troubleshooting**

### **Translations Not Showing**
- Did you run `python compile_translations.py`?
- Did you add `{% load i18n %}` at the top of the template?
- Did you wrap strings with `{% trans %}` tags?

### **Wrong Language Appearing**
- Check the URL prefix: `/en/`, `/fr/`, `/ar/`
- Clear browser cache (sometimes it caches language preference)
- Check `LANGUAGE_CODE` in settings.py

### **Missing .mo Files**
Run: `python compile_translations.py`

---

**Last Updated:** April 17, 2026  
**Language Support:** English, French, Arabic (Right-to-Left)
