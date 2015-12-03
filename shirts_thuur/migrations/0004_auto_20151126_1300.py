# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shirts_thuur', '0003_auto_20151126_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shirtpage',
            name='shirt_image',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='shirts_thuur.ShirtImage', null=True),
        ),
        migrations.AlterField(
            model_name='shirtrendition',
            name='image',
            field=models.ForeignKey(related_name='renditions', to='shirts_thuur.ShirtImage'),
        ),
    ]
