# topics.managers
# Managers for the topic models.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Tue Sep 08 20:26:17 2015 -0400
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: managers.py [] benjamin@bengfort.com $

"""
Managers for the topic models.
"""

##########################################################################
## Imports
##########################################################################

from django.db import models
from titlecase import titlecase
from qsstats import QuerySetStats

from datetime import timedelta
from django.utils import timezone
from django.template.defaultfilters import slugify

##########################################################################
## Topic Manager
##########################################################################

class TopicManager(models.Manager):
    """
    Helper functions for topic management
    """

    def from_title(self, title):
        """
        A get or create from a slug function.
        """
        # Titlecase the topic
        title = titlecase(title)

        # If the slug exists, return the object
        query = self.filter(slug=slugify(title))
        if query.exists():
            return query.first()

        # Otherwise create the topic with the title
        return self.create(title=title)

    def from_string(self, text):
        """
        Basically a get or create for a batch insert of topics separated by
        newlines as written into a text field or similar.
        """
        for line in frozenset(text.splitlines()):
            if line:
                yield self.from_title(line)

    def with_votes(self):
        """
        Annotates the topic model with a vote total.
        """
        return self.annotate(
            vote_total=models.Sum('votes__vote')
        )

    def mean_weight(self):
        """
        Returns the mean weight aggregation of all topics.
        """
        return self.with_votes().aggregate(
            mean_weight=models.Avg('vote_total')
        )['mean_weight']


##########################################################################
## Topic Manager
##########################################################################


class VotingManager(models.Manager):
    """
    Helper functions for vote management
    """

    def upvotes(self):
        """
        Returns the set of all up votes for a particular query.
        """
        return self.filter(vote=self.model.BALLOT.upvote)

    def downvotes(self):
        """
        Returns the set of all down votes for a particular query.
        """
        return self.filter(vote=self.model.BALLOT.downvote)

    def total(self):
        """
        Returns the sum of all up and down votes for a particular query.
        """
        return self.aggregate(
            total=models.Sum('vote')
        )

    def responses(self):
        """
        Returns an aggregation of IP address and the count per IP.
        """
        query = self.values("ipaddr")
        query = query.annotate(responses=models.Count('ipaddr'))
        query = query.order_by('ipaddr')
        return query

    def response_stats(self):
        """
        Returns a list of statistics from the responses histogram.
        """
        return self.responses().aggregate(
            num=models.Sum('responses'),
            avg=models.Avg('responses'),
            min=models.Min('responses'),
            max=models.Max('responses'),
        )

    def num_responses(self):
        """
        Returns the number of distinct IP addresses
        """
        return self.aggregate(r=models.Count('ipaddr', distinct=True))['r']

    def response_timeseries(self):
        """
        Returns a list of timeseries from the responses.
        """
        qss = QuerySetStats(self.all(), 'created')
        return qss.time_series(timezone.now() - timedelta(days=7), timezone.now())
