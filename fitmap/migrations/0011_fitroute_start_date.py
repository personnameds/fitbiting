# Generated by Django 2.2.3 on 2019-08-25 02:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitmap', '0010_remove_fitrunner_last_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='fitroute',
            name='start_date',
            field=models.DateField(default=datetime.date(2019, 8, 24)),
            preserve_default=False,
        ),
    ]
