# Gestion des Presences

Application Django pour gerer une salle de classe, ajouter des classes, inscrire des etudiants, enregistrer l'appel et exporter des rapports PDF.

## Nouvelles fonctionnalites

- Connexion enseignant avec l'authentification Django.
- Tableau de bord pour voir les classes, le nombre d'etudiants et l'activite du jour.
- Ajout de classes depuis l'interface web.
- Ajout d'etudiants depuis la page de chaque classe.
- Suivi des presences et absences cumulees par etudiant.
- Export PDF journalier apres l'appel.
- Export PDF mensuel par classe.

## Prerequis

- Python 3.11 ou plus recent
- Django 5.x
- reportlab

## Installation rapide

1. Installez les dependances :
```bash
pip install -r requirements.txt
```

2. Appliquez les migrations :
```bash
python manage.py migrate
```

3. Creez un compte enseignant :
```bash
python manage.py createsuperuser
```

4. Lancez le serveur :
```bash
python manage.py runserver
```

5. Ouvrez `http://127.0.0.1:8000/` puis connectez-vous avec votre compte.

## Base de donnees Supabase

L'application utilise maintenant Supabase/Postgres quand une variable `DATABASE_URL`
ou `SUPABASE_DB_HOST` est definie. Sans ces variables, elle continue d'utiliser
`db.sqlite3` en local.

1. Dans Supabase, ouvrez `Project Settings > Database` et copiez l'URI de connexion
   Postgres. Le mode pooler fonctionne bien pour une application web.

2. Creez un fichier `.env` a la racine du projet :
```bash
DATABASE_URL=postgresql://postgres.your-project-ref:your-password@aws-0-your-region.pooler.supabase.com:6543/postgres
```

3. Installez les dependances puis creez les tables dans Supabase :
```bash
pip install -r requirements.txt
python manage.py migrate
```

4. Pour copier les donnees deja presentes dans `db.sqlite3` vers Supabase :
```bash
python manage.py dumpdata --exclude contenttypes --exclude auth.permission --indent 2 > data.json
python manage.py loaddata data.json
```

Ne commitez jamais le fichier `.env`, il contient le mot de passe Supabase.

## Utilisation

1. Connectez-vous.
2. Ajoutez une ou plusieurs classes depuis le tableau de bord.
3. Ouvrez une classe pour ajouter des etudiants.
4. Cochez les presents puis cliquez sur `Enregistrer l'appel`.
5. Telechargez le rapport mensuel si besoin.

## Notes techniques

- La migration `0004_upgrade_classroom_management.py` ajoute les nouveaux champs pour mieux gerer les classes et les etudiants.
- Les totaux de presences et d'absences sont mis a jour automatiquement lors de l'enregistrement de l'appel.
