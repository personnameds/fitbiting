# Generated by Django 2.2.6 on 2019-11-15 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('runmap', '0003_route_total_distance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='total_distance',
            field=models.DecimalField(decimal_places=1, max_digits=7),
        ),
    ]