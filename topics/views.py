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
from topics.serializers import *
from topics.forms import MultiTopicForm

from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse

from rest_framework import viewsets
from rest_framework.response import Response

##########################################################################
## HTML/Django Views
##########################################################################

class ResultView(TemplateView):

    template_name = "site/results.html"

    def get_context_data(self, **kwargs):
        context = super(ResultView, self).get_context_data(**kwargs)
        # context['topics'] = json.dumps(list(Topic.objects.with_votes().values('title', 'vote_total')))
        return context


class MultiTopicView(FormView):

    template_name = "site/home.html"
    form_class    = MultiTopicForm

    def get_success_url(self):
        return reverse('results')

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(MultiTopicView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.save_topics()
        return super(MultiTopicView, self).form_valid(form)


##########################################################################
## API/DRF Views
##########################################################################

class TopicViewSet(viewsets.ViewSet):

    queryset = Topic.objects.with_votes().order_by('-vote_total')
    serializer_class = TopicSerializer

    def list(self, request):
        queryset = self.queryset.values('title', 'vote_total')[:300]
        return Response(queryset)
