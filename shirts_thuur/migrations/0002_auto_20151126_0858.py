# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailadmin.taggable
import modelcluster.fields
import wagtail.wagtailimages.models
import wagtail.wagtailcore.fields
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0008_image_created_at_index'),
        ('taggit', '0002_auto_20150616_2121'),
        ('wagtailcore', '0020_add_index_on_page_first_published_at'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shirts_thuur', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShirtImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('file', models.ImageField(height_field='height', upload_to=wagtail.wagtailimages.models.get_upload_to, width_field='width', verbose_name='File')),
                ('width', models.IntegerField(verbose_name='Width', editable=False)),
                ('height', models.IntegerField(verbose_name='Height', editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at', db_index=True)),
                ('focal_point_x', models.PositiveIntegerField(null=True, blank=True)),
                ('focal_point_y', models.PositiveIntegerField(null=True, blank=True)),
                ('focal_point_width', models.PositiveIntegerField(null=True, blank=True)),
                ('focal_point_height', models.PositiveIntegerField(null=True, blank=True)),
                ('file_size', models.PositiveIntegerField(null=True, editable=False)),
                ('caption', models.CharField(max_length=255, verbose_name='Caption')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text=None, verbose_name='Tags')),
                ('uploaded_by_user', models.ForeignKey(blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='Uploaded by user')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, wagtail.wagtailadmin.taggable.TagSearchable),
        ),
        migrations.CreateModel(
            name='ShirtIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('intro', wagtail.wagtailcore.fields.RichTextField(blank=True)),
            ],
            options={
                'verbose_name': 'Overzicht shirts',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ShirtPageRelatedLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField()),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ShirtRendition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.ImageField(height_field='height', width_field='width', upload_to='images')),
                ('width', models.IntegerField(editable=False)),
                ('height', models.IntegerField(editable=False)),
                ('focal_point_key', models.CharField(default='', max_length=255, editable=False, blank=True)),
                ('filter', models.ForeignKey(related_name='+', to='wagtailimages.Filter')),
                ('image', models.ForeignKey(related_name='rendition', to='shirts_thuur.ShirtImage')),
            ],
        ),
        migrations.AlterModelOptions(
            name='shirtpage',
            options={'verbose_name': 'Shirt pagina'},
        ),
        migrations.AddField(
            model_name='shirtpagerelatedlink',
            name='page',
            field=modelcluster.fields.ParentalKey(related_name='related_links', to='shirts_thuur.ShirtPage'),
        ),
        migrations.AlterUniqueTogether(
            name='shirtrendition',
            unique_together=set([('image', 'filter', 'focal_point_key')]),
        ),
    ]
