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
        for line in text.splitlines():
            if line:
                yield self.from_title(line)
