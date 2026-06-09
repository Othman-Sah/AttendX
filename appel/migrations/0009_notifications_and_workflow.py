import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appel', '0008_absencejustification_attachment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='absencejustification',
            name='reviewed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_justifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='absencejustification',
            name='teacher_comment',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='documentrequest',
            name='admin_comment',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='documentrequest',
            name='delivered_file',
            field=models.FileField(blank=True, null=True, upload_to='documents/'),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=140)),
                ('message', models.TextField()),
                ('level', models.CharField(choices=[('info', 'Information'), ('success', 'Succes'), ('warning', 'Alerte')], default='info', max_length=20)),
                ('link', models.CharField(blank=True, max_length=255)),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
