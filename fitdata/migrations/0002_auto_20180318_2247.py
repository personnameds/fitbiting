# Generated by Django 2.0.3 on 2018-03-18 22:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fitdata', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fitdata',
            options={'verbose_name': 'Fitbit Data', 'verbose_name_plural': 'Fitbit Data'},
        ),
        migrations.RenameField(
            model_name='fitdata',
            old_name='steps',
            new_name='distance',
        ),
    ]
