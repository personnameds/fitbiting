# Generated by Django 2.0.3 on 2018-03-31 01:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EndPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('lat', models.DecimalField(decimal_places=6, max_digits=10)),
                ('long', models.DecimalField(decimal_places=6, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='FitRoute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('end', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitmap.EndPoint')),
            ],
        ),
        migrations.CreateModel(
            name='StartPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('lat', models.DecimalField(decimal_places=6, max_digits=10)),
                ('long', models.DecimalField(decimal_places=6, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='WayPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('lat', models.DecimalField(decimal_places=6, max_digits=10)),
                ('long', models.DecimalField(decimal_places=6, max_digits=10)),
            ],
        ),
        migrations.AddField(
            model_name='fitroute',
            name='start',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitmap.StartPoint'),
        ),
        migrations.AddField(
            model_name='fitroute',
            name='waypoints',
            field=models.ManyToManyField(to='fitmap.WayPoint'),
        ),
    ]
