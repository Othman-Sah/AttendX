from pathlib import Path

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from .models import AbsenceJustification, ClassSchedule, DocumentRequest, Etudiant, Filiere


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Email"),
        widget=forms.TextInput(attrs={'placeholder': _("Email")}),
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': _("Password")}),
    )


class SignUpForm(forms.ModelForm):
    full_name = forms.CharField(
        label=_("Nom complet"),
        widget=forms.TextInput(attrs={'placeholder': _("Entrez votre nom complet tel qu'il existe dans la classe")}),
    )
    filiere = forms.ModelChoiceField(
        queryset=Filiere.objects.order_by('nom'),
        label=_("Classe"),
        empty_label=_("Choisissez votre classe"),
        widget=forms.Select(),
    )
    student_number = forms.CharField(
        required=False,
        label=_("Numero etudiant"),
        widget=forms.TextInput(attrs={'placeholder': _("Optionnel, mais recommande pour vous retrouver plus vite")}),
    )
    password1 = forms.CharField(
        label=_("Mot de passe"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': _("Creez un mot de passe")}),
    )
    password2 = forms.CharField(
        label=_("Confirmer le mot de passe"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': _("Retapez le mot de passe")}),
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': _("Nom d'utilisateur"),
            'email': _("Email"),
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': _("Choisissez un identifiant")}),
            'email': forms.EmailInput(attrs={'placeholder': _("Votre email")}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css_class = 'form-select' if isinstance(field.widget, forms.Select) else 'form-control'
            existing_class = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing_class} {css_class}".strip()

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_("Ce nom d'utilisateur existe deja."))
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        full_name = (cleaned_data.get('full_name') or '').strip()
        filiere = cleaned_data.get('filiere')
        student_number = (cleaned_data.get('student_number') or '').strip()

        if password1 and password2 and password1 != password2:
            self.add_error('password2', _("Les mots de passe ne correspondent pas."))

        student = None
        if full_name and filiere:
            students = Etudiant.objects.filter(
                nom__iexact=full_name,
                filiere=filiere,
            )
            if student_number:
                students = students.filter(numero_etudiant=student_number)

            matches = list(students[:2])
            if not matches:
                raise forms.ValidationError(_("Aucun etudiant correspondant n'a ete trouve dans cette classe."))

            if len(matches) > 1:
                self.add_error('student_number', _("Plusieurs etudiants portent ce nom. Ajoutez le numero etudiant."))
            else:
                student = matches[0]
                if student.user_id:
                    self.add_error('full_name', _("Cet etudiant a deja un compte."))

        self.student = student
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        first_name, *rest = self.cleaned_data['full_name'].split()
        user.first_name = first_name
        user.last_name = ' '.join(rest)
        if commit:
            user.save()
            if getattr(self, 'student', None):
                self.student.user = user
                self.student.email = self.cleaned_data.get('email') or self.student.email
                self.student.save(update_fields=['user', 'email'])
        return user


class FiliereForm(forms.ModelForm):
    teacher = forms.ModelChoiceField(
        queryset=User.objects.none(),
        required=False,
        label=_('Enseignant assigne'),
        empty_label=_('Choisir un enseignant'),
    )
    class_date = forms.DateField(
        required=False,
        label=_('Date du cours'),
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    day_of_week = forms.ChoiceField(
        choices=[('', _("Choisir un jour"))] + list(ClassSchedule.DAY_CHOICES),
        required=False,
        label=_("Jour"),
        widget=forms.HiddenInput(),
    )
    start_time = forms.TimeField(
        required=False,
        label=_("Heure de debut"),
        widget=forms.TimeInput(attrs={'type': 'time'}),
    )
    end_time = forms.TimeField(
        required=False,
        label=_("Heure de fin"),
        widget=forms.TimeInput(attrs={'type': 'time'}),
    )
    subject = forms.CharField(
        required=False,
        label=_("Matiere"),
        widget=forms.TextInput(attrs={'placeholder': _('Ex: Algorithmique')}),
    )
    session_type = forms.ChoiceField(
        choices=ClassSchedule.SESSION_TYPE_CHOICES,
        initial=ClassSchedule.SESSION_NORMAL,
        required=False,
        label=_("Session type"),
        widget=forms.Select(),
    )
    room = forms.CharField(
        required=False,
        label=_("Salle du cours"),
        widget=forms.TextInput(attrs={'placeholder': _('Ex: B12')}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teacher'].queryset = User.objects.filter(
            etudiant_profile__isnull=True,
        ).filter(
            Q(is_staff=False),
            Q(is_superuser=False),
        ).order_by('username')
        for field_name, field in self.fields.items():
            css_class = 'form-select' if isinstance(field.widget, forms.Select) else 'form-control'
            existing_class = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing_class} {css_class}".strip()

    def clean(self):
        cleaned_data = super().clean()
        class_date = cleaned_data.get('class_date')
        day_of_week = cleaned_data.get('day_of_week')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        subject = (cleaned_data.get('subject') or '').strip()

        has_schedule_data = any([class_date, start_time, end_time, subject])
        if class_date:
            cleaned_data['day_of_week'] = class_date.strftime('%A')
        elif has_schedule_data:
            self.add_error('class_date', _("Choisissez une date de cours."))

        if has_schedule_data:
            if not subject:
                self.add_error('subject', _("Entrez la matiere du cours."))
            if not start_time:
                self.add_error('start_time', _("Entrez l'heure de debut."))
            if not end_time:
                self.add_error('end_time', _("Entrez l'heure de fin."))

        if start_time and end_time and end_time <= start_time:
            self.add_error('end_time', _("L'heure de fin doit etre apres l'heure de debut."))

        return cleaned_data

    class Meta:
        model = Filiere
        fields = ['nom', 'salle', 'description', 'teacher']
        labels = {
            'nom': _('Nom de la classe'),
            'salle': _('Salle'),
            'description': _('Description'),
            'teacher': _('Enseignant assigne'),
        }
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': _('Ex: Informatique 2A')}),
            'salle': forms.TextInput(attrs={'placeholder': _('Ex: B12')}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': _('Quelques details sur la classe')}),
            'teacher': forms.Select(),
        }


class EtudiantForm(forms.ModelForm):
    ALLOWED_PHOTO_TYPES = {'image/jpeg', 'image/png', 'image/webp', 'image/gif'}
    MAX_PHOTO_SIZE = 10 * 1024 * 1024

    create_student_account = forms.BooleanField(
        required=False,
        label=_("Creer un compte etudiant"),
    )
    student_username = forms.CharField(
        required=False,
        label=_("Identifiant etudiant"),
        widget=forms.TextInput(attrs={'placeholder': _('Ex: aya.bennani')}),
    )
    student_password = forms.CharField(
        required=False,
        label=_("Mot de passe etudiant"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': _('Ex: etu12345')}),
    )

    class Meta:
        model = Etudiant
        fields = ['nom', 'numero_etudiant', 'email', 'profile_photo']
        labels = {
            'nom': _("Nom complet"),
            'numero_etudiant': _("Numero etudiant"),
            'email': _("Email"),
            'profile_photo': _("Photo de profil"),
        }
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': _('Ex: Salma El Idrissi')}),
            'numero_etudiant': forms.TextInput(attrs={'placeholder': _('Ex: STI-2026-014')}),
            'email': forms.EmailInput(attrs={'placeholder': _('Ex: etudiant@ecole.ma')}),
            'profile_photo': forms.FileInput(attrs={'accept': 'image/png,image/jpeg,image/webp,image/gif'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        create_student_account = cleaned_data.get('create_student_account')
        username = cleaned_data.get('student_username')
        password = cleaned_data.get('student_password')

        if create_student_account:
            if not username:
                self.add_error('student_username', _("Entrez un identifiant pour l'etudiant."))
            elif User.objects.filter(username=username).exists():
                self.add_error('student_username', _("Cet identifiant existe deja."))

            if not password:
                self.add_error('student_password', _("Entrez un mot de passe pour l'etudiant."))

        return cleaned_data

    def clean_profile_photo(self):
        photo = self.cleaned_data.get('profile_photo')
        if not photo:
            return photo

        content_type = getattr(photo, 'content_type', '')
        extension = Path(photo.name).suffix.lower()
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
        if content_type not in self.ALLOWED_PHOTO_TYPES and extension not in allowed_extensions:
            raise forms.ValidationError(_("Choisissez une image JPG, PNG, WEBP ou GIF."))

        if photo.size > self.MAX_PHOTO_SIZE:
            raise forms.ValidationError(_("La photo ne doit pas depasser 10 MB."))

        return photo


class ClassScheduleForm(forms.ModelForm):
    day_of_week = forms.ChoiceField(
        choices=[('', _("Choisir un jour"))] + list(ClassSchedule.DAY_CHOICES),
        required=False,
        label=_("Jour"),
        widget=forms.HiddenInput(),
    )
    session_type = forms.ChoiceField(
        choices=ClassSchedule.SESSION_TYPE_CHOICES,
        required=False,
        label=_("Session type"),
        widget=forms.Select(),
    )

    class Meta:
        model = ClassSchedule
        fields = ['class_date', 'day_of_week', 'start_time', 'end_time', 'subject', 'session_type', 'room']
        labels = {
            'class_date': _("Date du cours"),
            'day_of_week': _("Jour"),
            'start_time': _("Heure de debut"),
            'end_time': _("Heure de fin"),
            'subject': _("Matiere"),
            'session_type': _("Session type"),
            'room': _("Salle"),
        }
        widgets = {
            'class_date': forms.DateInput(attrs={'type': 'date'}),
            'day_of_week': forms.HiddenInput(),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'subject': forms.TextInput(attrs={'placeholder': _('Ex: Algorithmique')}),
            'session_type': forms.Select(),
            'room': forms.TextInput(attrs={'placeholder': _('Ex: B12')}),
        }

    def clean(self):
        cleaned_data = super().clean()
        class_date = cleaned_data.get('class_date')
        day_of_week = cleaned_data.get('day_of_week')
        session_type = cleaned_data.get('session_type')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if class_date:
            cleaned_data['day_of_week'] = class_date.strftime('%A')
        elif not day_of_week:
            self.add_error('class_date', _("Choisissez une date de cours."))

        if not session_type:
            cleaned_data['session_type'] = ClassSchedule.SESSION_NORMAL

        if start_time and end_time and end_time <= start_time:
            self.add_error('end_time', _("L'heure de fin doit etre apres l'heure de debut."))

        return cleaned_data


class AbsenceJustificationForm(forms.ModelForm):
    MAX_UPLOAD_SIZE = 5 * 1024 * 1024

    class Meta:
        model = AbsenceJustification
        fields = ['reason', 'details', 'attachment']
        labels = {
            'reason': _("Motif"),
            'details': _("Explication"),
            'attachment': _("Piece jointe"),
        }
        widgets = {
            'reason': forms.TextInput(attrs={'placeholder': _('Ex: Rendez-vous medical')}),
            'details': forms.Textarea(attrs={'rows': 4, 'placeholder': _("Ajoutez plus de details sur l'absence")}),
            'attachment': forms.FileInput(attrs={'accept': '.pdf,image/*'}),
        }

    def clean_attachment(self):
        attachment = self.cleaned_data.get('attachment')
        if not attachment:
            return attachment

        extension = Path(attachment.name).suffix.lower()
        allowed_extensions = {'.pdf', '.png', '.jpg', '.jpeg', '.gif', '.webp'}

        if extension not in allowed_extensions:
            raise forms.ValidationError(_("Ajoutez un fichier PDF ou une image valide."))

        if attachment.size > self.MAX_UPLOAD_SIZE:
            raise forms.ValidationError(_("Le fichier ne doit pas depasser 5 MB"))

        return attachment


class ImportExcelForm(forms.Form):
    """Form pour importer une liste d'etudiants depuis un fichier Excel"""

    MAX_UPLOAD_SIZE = 5 * 1024 * 1024

    excel_file = forms.FileField(
        label=_("Fichier Excel"),
        help_text=_("Formats acceptes: .xlsx, .xls"),
        widget=forms.FileInput(attrs={'accept': '.xlsx,.xls'}),
    )

    def clean_excel_file(self):
        file = self.cleaned_data.get('excel_file')
        if file:
            extension = Path(file.name).suffix.lower()
            if extension not in {'.xlsx', '.xls'}:
                raise forms.ValidationError(_("Veuillez uploader un fichier Excel (.xlsx ou .xls)"))
            if file.size > self.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_("Le fichier ne doit pas depasser 5 MB"))
        return file


class ImportClassesExcelForm(forms.Form):
    """Form pour importer une liste de classes depuis un fichier Excel"""

    MAX_UPLOAD_SIZE = 5 * 1024 * 1024

    excel_file = forms.FileField(
        label=_("Fichier Excel des classes"),
        help_text=_("Formats acceptes: .xlsx, .xls"),
        widget=forms.FileInput(attrs={'accept': '.xlsx,.xls'}),
    )

    def clean_excel_file(self):
        file = self.cleaned_data.get('excel_file')
        if file:
            extension = Path(file.name).suffix.lower()
            if extension not in {'.xlsx', '.xls'}:
                raise forms.ValidationError(_("Veuillez uploader un fichier Excel (.xlsx ou .xls)"))
            if file.size > self.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_("Le fichier ne doit pas depasser 5 MB"))
        return file


class PasswordChangeForm(forms.Form):
    """Form for changing user password"""

    current_password = forms.CharField(
        label=_("Mot de passe actuel"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': _("Entrez votre mot de passe actuel"),
            'class': 'form-control',
        }),
    )
    new_password1 = forms.CharField(
        label=_("Nouveau mot de passe"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': _("Entrez votre nouveau mot de passe"),
            'class': 'form-control',
        }),
    )
    new_password2 = forms.CharField(
        label=_("Confirmez le nouveau mot de passe"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': _("Confirmez votre nouveau mot de passe"),
            'class': 'form-control',
        }),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise forms.ValidationError(_("Le mot de passe actuel est incorrect."))
        return current_password

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError(_("Les nouveaux mots de passe ne correspondent pas."))
            if len(new_password1) < 6:
                raise forms.ValidationError(_("Le nouveau mot de passe doit contenir au moins 6 caracteres."))

        return cleaned_data


class UserProfileUpdateForm(forms.ModelForm):
    """Form for updating user profile information"""
    ALLOWED_PHOTO_TYPES = {'image/jpeg', 'image/png', 'image/webp', 'image/gif'}
    MAX_PHOTO_SIZE = 10 * 1024 * 1024

    first_name = forms.CharField(
        label=_("Prénom"),
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': _("Votre prénom"),
            'class': 'form-control',
        }),
    )
    last_name = forms.CharField(
        label=_("Nom de famille"),
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': _("Votre nom de famille"),
            'class': 'form-control',
        }),
    )
    email = forms.EmailField(
        label=_("Email"),
        required=False,
        widget=forms.EmailInput(attrs={
            'placeholder': _("Votre adresse email"),
            'class': 'form-control',
        }),
    )
    profile_photo = forms.FileField(
        label=_("Photo de profil"),
        required=False,
        widget=forms.FileInput(attrs={
            'accept': 'image/png,image/jpeg,image/webp,image/gif',
            'class': 'form-control',
        }),
        help_text=_("Formats acceptes: JPG, PNG, WEBP ou GIF. Taille maximale: 10 MB."),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(_("Cet email est déjà utilisé par un autre compte."))
        return email

    def clean_profile_photo(self):
        photo = self.cleaned_data.get('profile_photo')
        if not photo:
            return photo

        content_type = getattr(photo, 'content_type', '')
        extension = Path(photo.name).suffix.lower()
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
        if content_type not in self.ALLOWED_PHOTO_TYPES and extension not in allowed_extensions:
            raise forms.ValidationError(_("Choisissez une image JPG, PNG, WEBP ou GIF."))

        if photo.size > self.MAX_PHOTO_SIZE:
            raise forms.ValidationError(_("La photo ne doit pas depasser 10 MB."))

        return photo


class DocumentRequestForm(forms.ModelForm):
    class Meta:
        model = DocumentRequest
        fields = ['document_type', 'comments']
        labels = {
            'document_type': _("Type de document"),
            'comments': _("Commentaire"),
        }
        widgets = {
            'document_type': forms.Select(
                choices=[
                    ('', _("Choisir un type...")),
                    (_("Attestation de scolarite"), _("Attestation de scolarite")),
                    (_("Releve de notes"), _("Releve de notes")),
                    (_("Certificat de presence"), _("Certificat de presence")),
                    (_("Autre"), _("Autre")),
                ],
                attrs={'class': 'form-select'},
            ),
            'comments': forms.Textarea(
                attrs={'rows': 3, 'placeholder': _('Precisez si besoin...'), 'class': 'form-control'}
            ),
        }


class JustificationReviewForm(forms.Form):
    ACTION_APPROVE = 'approve'
    ACTION_REJECT = 'reject'

    justification_id = forms.IntegerField(widget=forms.HiddenInput())
    action = forms.ChoiceField(
        choices=[
            (ACTION_APPROVE, _("Approuver")),
            (ACTION_REJECT, _("Rejeter")),
        ],
        widget=forms.HiddenInput(),
        required=False,
    )
    teacher_comment = forms.CharField(
        required=False,
        label=_("Commentaire enseignant"),
        widget=forms.Textarea(
            attrs={'rows': 3, 'placeholder': _("Ajouter un commentaire pour l'etudiant"), 'class': 'form-control'}
        ),
    )


class DocumentProcessingForm(forms.Form):
    ACTION_PROCESS = 'process'
    ACTION_READY = 'ready'
    ACTION_REJECT = 'reject'

    request_id = forms.IntegerField(widget=forms.HiddenInput())
    action = forms.ChoiceField(
        choices=[
            (ACTION_PROCESS, _("Mettre en traitement")),
            (ACTION_READY, _("Marquer pret")),
            (ACTION_REJECT, _("Refuser")),
        ],
        widget=forms.HiddenInput(),
        required=False,
    )
    admin_comment = forms.CharField(
        required=False,
        label=_("Commentaire administratif"),
        widget=forms.Textarea(
            attrs={'rows': 3, 'placeholder': _("Ajouter une reponse ou une consigne"), 'class': 'form-control'}
        ),
    )
    delivered_file = forms.FileField(
        required=False,
        label=_("Fichier livre"),
        widget=forms.FileInput(attrs={'accept': '.pdf,image/*', 'class': 'form-control'}),
    )
