# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('title', models.CharField(max_length=128)),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'title', unique=True, editable=False)),
                ('link', models.URLField(default=None, null=True, blank=True)),
            ],
            options={
                'ordering': ('-created',),
                'db_table': 'topics',
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('vote', models.SmallIntegerField(default=1, choices=[(-1, b'downvote'), (1, b'upvote'), (0, b'novote')])),
                ('ipaddr', models.GenericIPAddressField()),
                ('topic', models.ForeignKey(related_name='votes', to='topics.Topic')),
            ],
            options={
                'ordering': ('-created',),
                'db_table': 'voting',
            },
        ),
    ]
