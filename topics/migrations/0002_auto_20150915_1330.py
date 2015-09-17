# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='is_canonical',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='topic',
            name='refers_to',
            field=models.ForeignKey(related_name='references', default=None, blank=True, to='topics.Topic', null=True),
        ),
    ]
