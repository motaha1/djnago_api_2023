# Generated by Django 3.0.3 on 2022-11-28 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0011_auto_20221128_0331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='upload',
            field=models.ImageField(null=True, upload_to='images/%y/%m/%d'),
        ),
    ]
