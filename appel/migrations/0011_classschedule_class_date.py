from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appel', '0010_filiere_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='classschedule',
            name='class_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
