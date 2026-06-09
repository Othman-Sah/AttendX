import uuid

from django.db import models
from django.db.models import Count, Q
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Filiere(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    salle = models.CharField(max_length=50, blank=True)
    teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='assigned_filieres',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

class Etudiant(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='etudiant_profile')
    nom = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    numero_etudiant = models.CharField(max_length=30, blank=True, null=True)
    profile_photo = models.FileField(upload_to='profiles/', blank=True, null=True)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name='etudiants')
    total_presences = models.PositiveIntegerField(default=0)
    total_absences = models.PositiveIntegerField(default=0)
    date_inscription = models.DateField(default=now)

    def __str__(self):
        return self.nom

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['filiere', 'numero_etudiant'],
                name='unique_student_number_per_class',
            ),
        ]

    def refresh_attendance_totals(self, save=True):
        """Recompute attendance counters from the related presence records."""
        totals = self.presences.aggregate(
            present_count=Count('id', filter=Q(present=True)),
            absent_count=Count('id', filter=Q(present=False)),
        )
        self.total_presences = totals['present_count'] or 0
        self.total_absences = totals['absent_count'] or 0

        if save:
            self.save(update_fields=['total_presences', 'total_absences'])

        return self.total_presences, self.total_absences

class Presence(models.Model):
    etudiant = models.ForeignKey('Etudiant', on_delete=models.CASCADE, related_name='presences')
    date = models.DateField(default=now)
    present = models.BooleanField()

    class Meta:
        unique_together = ('etudiant', 'date')
        ordering = ['-date', 'etudiant__nom']

    def __str__(self):
        return f"{self.etudiant.nom} - {'Present' if self.present else 'Absent'} le {self.date}"


class AbsenceJustification(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'

    STATUS_CHOICES = [
        (STATUS_PENDING, _('En attente')),
        (STATUS_APPROVED, _('Approuvee')),
        (STATUS_REJECTED, _('Refusee')),
    ]

    presence = models.OneToOneField(Presence, on_delete=models.CASCADE, related_name='justification')
    reason = models.CharField(max_length=150)
    details = models.TextField()
    attachment = models.FileField(upload_to='justifications/', blank=True, null=True)
    teacher_comment = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='reviewed_justifications',
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"Justification {self.presence.etudiant.nom} - {self.presence.date}"

    def review(self, status, reviewed_by=None, teacher_comment=''):
        self.status = status
        self.reviewed_by = reviewed_by
        self.teacher_comment = teacher_comment
        self.reviewed_at = now()
        self.save(update_fields=['status', 'reviewed_by', 'teacher_comment', 'reviewed_at'])


class DocumentRequest(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_PROCESSING = 'processing'
    STATUS_READY = 'ready'
    STATUS_REJECTED = 'rejected'

    STATUS_CHOICES = [
        (STATUS_PENDING, _('En attente')),
        (STATUS_PROCESSING, _('En traitement')),
        (STATUS_READY, _('Pret')),
        (STATUS_REJECTED, _('Refuse')),
    ]

    etudiant = models.ForeignKey('Etudiant', on_delete=models.CASCADE, related_name='document_requests')
    document_type = models.CharField(max_length=100)
    comments = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    request_date = models.DateTimeField(auto_now_add=True)
    processed_date = models.DateTimeField(blank=True, null=True)
    admin_comment = models.TextField(blank=True)
    delivered_file = models.FileField(upload_to='documents/', blank=True, null=True)

    class Meta:
        ordering = ['-request_date']

    def __str__(self):
        return f"{self.etudiant.nom} - {self.document_type}"

    def update_status(self, status, admin_comment='', delivered_file=None):
        self.status = status
        self.admin_comment = admin_comment
        self.processed_date = now()
        if delivered_file:
            self.delivered_file = delivered_file
            self.save()
            return
        self.save(update_fields=['status', 'admin_comment', 'processed_date'])


class Notification(models.Model):
    LEVEL_INFO = 'info'
    LEVEL_SUCCESS = 'success'
    LEVEL_WARNING = 'warning'

    LEVEL_CHOICES = [
        (LEVEL_INFO, _('Information')),
        (LEVEL_SUCCESS, _('Succes')),
        (LEVEL_WARNING, _('Alerte')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=140)
    message = models.TextField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default=LEVEL_INFO)
    link = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class ClassSchedule(models.Model):
    """Schedule/Timetable for classes"""
    SESSION_NORMAL = 'normal'
    SESSION_EXAM = 'exam'
    SESSION_TYPE_CHOICES = [
        (SESSION_NORMAL, _('Normal class')),
        (SESSION_EXAM, _('Exam')),
    ]

    DAY_CHOICES = [
        ('Monday', _('Lundi')),
        ('Tuesday', _('Mardi')),
        ('Wednesday', _('Mercredi')),
        ('Thursday', _('Jeudi')),
        ('Friday', _('Vendredi')),
        ('Saturday', _('Samedi')),
    ]

    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name='schedules')
    class_date = models.DateField(blank=True, null=True)
    day_of_week = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject = models.CharField(max_length=100, help_text=_("Subject or course name"))
    session_type = models.CharField(
        max_length=20,
        choices=SESSION_TYPE_CHOICES,
        default=SESSION_NORMAL,
    )
    professor = models.CharField(max_length=100, blank=True)
    room = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['day_of_week', 'start_time']
        unique_together = ('filiere', 'day_of_week', 'start_time', 'end_time')

    def __str__(self):
        return f"{self.filiere.nom} - {self.day_of_week} {self.start_time}"


class QRAttendanceSession(models.Model):
    """A time-limited QR code session for contactless attendance marking."""
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name='qr_sessions')
    token = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_qr_sessions')
    date = models.DateField(default=now)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"QR {self.filiere.nom} {self.date}"

    def is_valid(self):
        return now() < self.expires_at
