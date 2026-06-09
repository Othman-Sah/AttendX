def app_shell(request):
    unread_count = 0
    student_profile = None

    if getattr(request, 'user', None) and request.user.is_authenticated:
        student_profile = getattr(request.user, 'etudiant_profile', None)
        unread_count = request.user.notifications.filter(is_read=False).count()

    if getattr(request, 'user', None) and request.user.is_authenticated:
        if student_profile:
            role = 'student'
        elif request.user.is_staff or request.user.is_superuser:
            role = 'admin'
        else:
            role = 'teacher'
    else:
        role = 'guest'

    return {
        'app_logo_url': '/logo/?v=logo2-jpeg',
        'app_unread_notification_count': unread_count,
        'app_is_student': bool(student_profile),
        'app_is_admin': bool(getattr(request.user, 'is_staff', False) or getattr(request.user, 'is_superuser', False)),
        'app_is_teacher': role == 'teacher',
        'app_role': role,
    }
