# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-16 18:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('internet_shop', '0017_auto_20180114_2013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='parent',
        ),
        migrations.AlterField(
            model_name='userbasketitems',
            name='color',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='color_in_basket', to='internet_shop.Colors'),
        ),
        migrations.AlterField(
            model_name='userbasketitems',
            name='size',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='size_in_basket', to='internet_shop.Sizes'),
        ),
    ]
