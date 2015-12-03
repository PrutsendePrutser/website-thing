# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shirts_thuur', '0002_auto_20151126_0858'),
    ]

    operations = [
        migrations.CreateModel(
            name='InterestingThing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(null=True, blank=True)),
                ('text', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ShirtPageRefPlacement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('page', modelcluster.fields.ParentalKey(related_name='ref_placements', to='shirts_thuur.ShirtPage')),
                ('ref', models.ForeignKey(related_name='+', to='shirts_thuur.InterestingThing')),
            ],
            options={
                'verbose_name': 'Interesting reference',
                'verbose_name_plural': 'Interesting references',
            },
        ),
        migrations.AddField(
            model_name='shirtpage',
            name='interesting_ref',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='shirts_thuur.InterestingThing', null=True),
        ),
    ]
