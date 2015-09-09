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
from model_utils import Choices
from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel
from topics.managers import TopicManager, VotingManager

##########################################################################
## Topic Models
##########################################################################

class Topic(TimeStampedModel):
    """
    Stores a topic, basically a string like a tag and manages it.
    """

    # Topic fields
    title   = models.CharField(max_length=128)
    slug    = AutoSlugField(populate_from='title', unique=True)
    link    = models.URLField(null=True, blank=True, default=None)

    # Custom topic manager
    objects = TopicManager()

    # Topic meta class
    class Meta:
        db_table = 'topics'
        ordering = ('-created',)

    def __unicode__(self):
        return self.title

    def vote_total(self):
        """
        Accumulates the votes via aggregation
        """
        return self.votes.aggregate(
            total=models.Sum('vote')
        )['total']

##########################################################################
## Topic Voting
##########################################################################

class Vote(TimeStampedModel):
    """
    Simple voting model that stores an up or down vote for a particular topic
    associated with a particular IP address (and time of day).
    """

    DATEFMT  = "%a %b %d, %Y at %H:%M"
    BALLOT   = Choices((-1, 'downvote', 'downvote'), (1, 'upvote', 'upvote'), (0, 'novote', 'novote'))

    # Vote fields
    vote    = models.SmallIntegerField(choices=BALLOT, default=BALLOT.upvote)
    topic   = models.ForeignKey(Topic, related_name='votes')
    ipaddr  = models.GenericIPAddressField()

    # Custom voting manager
    objects = VotingManager()

    # Vote meta class
    class Meta:
        db_table = 'voting'
        ordering = ('-created',)

    def __unicode__(self):
        action = {
            -1: "-1",
             0: "--",
             1: "+1",
        }[self.vote]

        return "{} for \"{}\" ({} on {})".format(
            action, self.topic, self.ipaddr, self.modified.strftime(self.DATEFMT)
        )
