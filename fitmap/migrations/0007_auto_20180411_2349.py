# Generated by Django 2.0.3 on 2018-04-11 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitmap', '0006_auto_20180411_0032'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='waypoint',
            name='complete',
        ),
        migrations.AddField(
            model_name='fitmappedrte',
            name='num_complete_waypt',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]