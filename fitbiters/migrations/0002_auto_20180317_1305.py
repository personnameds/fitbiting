# Generated by Django 2.0.3 on 2018-03-17 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitbiters', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fitbiter',
            name='access_token',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='fitbiter',
            name='refresh_token',
            field=models.CharField(max_length=255),
        ),
    ]
