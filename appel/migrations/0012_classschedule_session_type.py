from django.db import migrations, models
import django.utils.translation


class Migration(migrations.Migration):

    dependencies = [
        ('appel', '0011_classschedule_class_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='classschedule',
            name='session_type',
            field=models.CharField(
                choices=[
                    ('normal', django.utils.translation.gettext_lazy('Normal class')),
                    ('exam', django.utils.translation.gettext_lazy('Exam')),
                ],
                default='normal',
                max_length=20,
            ),
        ),
    ]
