# Generated by Django 2.2.3 on 2019-08-21 21:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fitmap', '0005_fitroute_last_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='fitroute',
            name='finished',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='fitmappedrte',
            name='fitrunner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitmap.FitRunner'),
        ),
    ]