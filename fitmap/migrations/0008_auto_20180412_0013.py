# Generated by Django 2.0.3 on 2018-04-12 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitmap', '0007_auto_20180411_2349'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fitmappedrte',
            name='num_complete_waypt',
        ),
        migrations.AddField(
            model_name='fitroute',
            name='num_complete_waypt',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]