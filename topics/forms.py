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
from topics.models import Topic, Vote
from ipware.ip import get_real_ip, get_ip

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

    def save_topics(self):
        for topic in Topic.objects.from_string(self.cleaned_data['topics']):
            Vote.objects.create(topic=topic, ipaddr=self.ipaddr)
