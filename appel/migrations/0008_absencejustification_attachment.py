from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appel', '0007_documentrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='absencejustification',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='justifications/'),
        ),
    ]
