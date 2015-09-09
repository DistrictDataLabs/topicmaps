# topics.views
# Views for the Topics application
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Tue Sep 08 21:13:19 2015 -0400
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: views.py [] benjamin@bengfort.com $

"""
Views for the Topics application
"""

##########################################################################
## Imports
##########################################################################

from topics.models import Topic
from topics.forms import MultiTopicForm

from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse

##########################################################################
## HTML/Django Views
##########################################################################

class ResultView(TemplateView):

    template_name = "site/results.html"

    def get_context_data(self, **kwargs):
        context = super(ResultView, self).get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()
        return context


class MultiTopicView(FormView):

    template_name = "site/home.html"
    form_class    = MultiTopicForm

    def get_success_url(self):
        return reverse('results')

    def form_valid(self, form):
        form.save_topics()
        return super(MultiTopicView, self).form_valid(form)
