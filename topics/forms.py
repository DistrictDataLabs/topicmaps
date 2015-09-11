# topics.forms
# Forms for simple management of topics in Django.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Tue Sep 08 21:14:42 2015 -0400
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: forms.py [] benjamin@bengfort.com $

"""
Forms for simple management of topics in Django.
"""

##########################################################################
## Imports
##########################################################################

from django import forms
from collections import Counter
from topics.models import Topic, Vote
from ipware.ip import get_real_ip, get_ip
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify

##########################################################################
## Topic Management Forms
##########################################################################


class MultiTopicForm(forms.Form):
    """
    Post multiple topics separated by newlines.
    """

    topics = forms.CharField(
        widget=forms.Textarea, required=True,
        help_text="Enter multiple topics each on their own line."
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MultiTopicForm, self).__init__(*args, **kwargs)

    @property
    def ipaddr(self):
        """
        Get the IP Address of the form submitter via the request.
        """
        if not hasattr(self, '_ipaddr'):
            self._ipaddr = get_real_ip(self.request) or get_ip(self.request)
        return self._ipaddr

    def clean_topics(self):
        """
        Run validation for topics form.
        """

        data   = self.cleaned_data['topics']
        topics = filter(lambda x: x, [slugify(t) for t in data.splitlines()])

        # Check if there are commas or semicolons in the field.
        if "," in data or ";" in data or "|" in data:
            raise forms.ValidationError(
                _("This form is not comma, semicolon, or pipe delimited!"),
                code="bad_delimiter"
            )

        # Ensure at least two topics are submitted.
        if len(topics) < 2:
            raise forms.ValidationError(
                _("Please provide at least 2 topics, techniques, or technologies!"),
                code="single_topic_error"
            )

        # 50 topics is too many.
        if len(topics) > 50:
            raise forms.ValidationError(
                _("Thanks for thinking of so many topics! To prevent spam, however, "
                  "we have to limit you to 50 topics per form submission."),
                code="topic_spam_error"
            )

        # Ensure topic uniqueness in submission.
        if len(frozenset(topics)) < len(topics):
            raise forms.ValidationError(
                _("Duplicate topics detected! Please check your list and try again."),
                code="duplicate_topics"
            )

        return data

    def save_topics(self):
        """
        Write the topics and their votes to disk.
        """
        for topic in Topic.objects.from_string(self.cleaned_data['topics']):
            Vote.objects.create(topic=topic, ipaddr=self.ipaddr)
