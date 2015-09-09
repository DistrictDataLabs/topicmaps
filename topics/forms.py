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
from topics.models import Topic

##########################################################################
## Topic Management Forms
##########################################################################

class MultiTopicForm(forms.Form):
    """
    Post multiple topics separated by newlines.
    """

    topics = forms.CharField(
        widget=forms.Textarea, required=True,
        help_text="Enter multiple topics, separated by a new line."
    )

    def save_topics(self):
        return list(Topic.objects.from_string(self.cleaned_data['topics']))
