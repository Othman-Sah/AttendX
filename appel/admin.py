from django.contrib import admin

from .models import AbsenceJustification, ClassSchedule, DocumentRequest, Etudiant, Filiere, Notification, Presence


@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'teacher', 'salle', 'created_at')
    search_fields = ('nom', 'salle', 'teacher__username', 'teacher__first_name', 'teacher__last_name')


@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'numero_etudiant', 'filiere', 'user', 'total_presences', 'total_absences')
    list_filter = ('filiere',)
    search_fields = ('nom', 'numero_etudiant', 'email')


@admin.register(Presence)
class PresenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'etudiant', 'date', 'present')
    list_filter = ('date', 'present', 'etudiant__filiere')


@admin.register(AbsenceJustification)
class AbsenceJustificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'presence', 'reason', 'status', 'reviewed_by', 'submitted_at')
    list_filter = ('status', 'submitted_at')
    search_fields = ('presence__etudiant__nom', 'reason', 'details')


@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'filiere', 'class_date', 'day_of_week', 'start_time', 'end_time', 'subject', 'session_type', 'professor')
    list_filter = ('filiere', 'class_date', 'day_of_week', 'session_type')
    search_fields = ('subject', 'professor', 'filiere__nom')
    ordering = ('class_date', 'day_of_week', 'start_time')


@admin.register(DocumentRequest)
class DocumentRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'etudiant', 'document_type', 'status', 'request_date', 'processed_date')
    list_filter = ('status', 'request_date')
    search_fields = ('etudiant__nom', 'document_type', 'comments', 'admin_comment')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'level', 'is_read', 'created_at')
    list_filter = ('level', 'is_read', 'created_at')
    search_fields = ('user__username', 'title', 'message')
