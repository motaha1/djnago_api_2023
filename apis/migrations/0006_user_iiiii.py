# Generated by Django 3.0.3 on 2022-11-27 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0005_remove_user_iiiii'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='iiiii',
            field=models.CharField(blank=True, max_length=555, null=True),
        ),
    ]
