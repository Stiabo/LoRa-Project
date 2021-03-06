# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-10 13:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0002_temperature'),
    ]

    operations = [
        migrations.CreateModel(
            name='tagDetection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.IntegerField()),
                ('codeID', models.IntegerField()),
                ('codeData', models.IntegerField()),
                ('snr', models.IntegerField()),
                ('millisec', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TBR_sensorData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp', models.DecimalField(decimal_places=4, max_digits=10)),
                ('timestamp', models.IntegerField()),
                ('noise', models.IntegerField()),
                ('noiseLP', models.IntegerField()),
                ('freq', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Temperature',
        ),
    ]
