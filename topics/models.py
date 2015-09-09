# topics.models
# Topic modeling for data survey analysis
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Tue Sep 08 19:43:58 2015 -0400
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: models.py [] benjamin@bengfort.com $

"""
Topic modeling for data survey analysis
"""

##########################################################################
## Imports
##########################################################################

from django.db import models
from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel
from topics.managers import TopicManager

##########################################################################
## Topic Models
##########################################################################

class Topic(TimeStampedModel):
    """
    Stores a topic, basically a string like a tag and manages it.
    """

    # Topic fields
    title = models.CharField(max_length=128)
    slug  = AutoSlugField(populate_from='title', unique=True)
    link  = models.URLField(null=True, blank=True, default=None)

    # Custom topic manager
    objects = TopicManager()

    # Topic meta class
    class Meta:
        db_table = 'topics'
        ordering = ('-created',)

    def __unicode__(self):
        return self.title
