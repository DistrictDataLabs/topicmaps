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

import json
import random

from topics.serializers import *
from topics.models import Topic, Vote
from topics.forms import MultiTopicForm

from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import APIException

##########################################################################
## HTML/Django Views
##########################################################################

class ResultView(TemplateView):

    template_name = "site/results.html"

    def get_context_data(self, **kwargs):
        context = super(ResultView, self).get_context_data(**kwargs)

        # Compute statistics for view
        context['num_topics'] = Topic.objects.count()
        context['avg_topic_weight'] = Topic.objects.mean_weight()
        context['num_responses'] = Vote.objects.num_responses()

        stats = Vote.objects.response_stats()
        context['avg_topics_per_response'] = stats['avg']
        context['min_topics_per_response'] = stats['min']
        context['max_topics_per_response'] = stats['max']
        context['time_series'] = json.dumps([
            {'date': d.strftime("%Y-%m-%d"), 'count': c}
            for (d,c) in Vote.objects.response_timeseries()
        ])

        return context


class MultiTopicView(FormView):

    template_name = "site/survey.html"
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

class BadParameter(APIException):

    status_code    = 400
    default_detail = 'Bad parameter passed into GET request.'


class TopicViewSet(viewsets.ViewSet):

    queryset = Topic.objects.with_votes()
    serializer_class = TopicSerializer
    permission_classes = (AllowAny,)

    def random_topics(self, limit=10):
        last = Topic.objects.count() - 1
        indices = random.sample(xrange(0, last), limit)

        for idx in indices:
            yield self.queryset.values('title', 'vote_total')[idx]

    def list(self, request):
        try:
            limit    = int(self.request.query_params.get('limit', 300))
            ordering = self.request.query_params.get('ordering', '-vote_total').lower()

            if ordering == 'random':
                return Response(list(self.random_topics(limit)))

            queryset = self.queryset.order_by(ordering)
            queryset = queryset.values('title', 'vote_total')[:limit]
            return Response(list(queryset))
        except Exception as e:
            raise BadParameter(str(e))
