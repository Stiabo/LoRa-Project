# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-10 13:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temperature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp', models.DecimalField(decimal_places=4, max_digits=10)),
                ('timestamp', models.IntegerField()),
                ('tag_id', models.IntegerField()),
            ],
        ),
    ]
