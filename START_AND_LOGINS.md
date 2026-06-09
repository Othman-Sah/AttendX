# AttendX - Start Guide and Logins

## Start the project

Open PowerShell in this folder:

```powershell
cd "C:\Users\xyzha\Desktop\ATTENDX WEB"
```

Run the Django server:

```powershell
python.exe manage.py runserver 127.0.0.1:8000 --settings=gestion_presence.settings
```

Then open:

```text
http://127.0.0.1:8000/
```

Useful direct pages:

```text
Login:  http://127.0.0.1:8000/fr/login/
Signup: http://127.0.0.1:8000/fr/signup/
Admin:  http://127.0.0.1:8000/admin/
```

## If dependencies are missing

```powershell
python.exe -m pip install -r requirements.txt
```

## If database tables are missing

```powershell
python.exe manage.py migrate --settings=gestion_presence.settings
```

## Known working logins

| Role | Username | Password | Notes |
| --- | --- | --- | --- |
| Teacher | `othman` | `prof1234` | Working local account |
| Teacher demo | `prof` | `prof1234` | Working local account |

## Other users in the local database

These accounts exist, but their plain-text passwords cannot be read because Django stores password hashes.

| Username | Name | Email | Staff | Superuser |
| --- | --- | --- | --- | --- |
| `admin` |  |  | Yes | Yes |
| `admin-test` |  |  | Yes | No |
| `haythame.amattouch` | HAYTHAME AMATTOUCH | haythame.amattouch@example.com | No | No |
| `haythame.duplicate` | HAYTHAME AMATTOUCH | haythame.amattouch@example.com | No | No |
| `kevinomgba` |  | kevinomgba1@gmail.com | Yes | Yes |

## Reset a password

Use this if you need access to an account with an unknown password:

```powershell
python.exe manage.py changepassword USERNAME --settings=gestion_presence.settings
```

Example:

```powershell
python.exe manage.py changepassword admin --settings=gestion_presence.settings
```

## Create a new admin login

```powershell
python.exe manage.py createsuperuser --settings=gestion_presence.settings
```

## Stop an old local server

If another Django project is already using port 8000, stop it first or use a different port:

```powershell
python.exe manage.py runserver 127.0.0.1:8001 --settings=gestion_presence.settings
```
