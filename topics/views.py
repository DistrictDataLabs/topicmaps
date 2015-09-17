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

import csv
import random

from topics.serializers import *
from topics.models import Topic, Vote
from topics.forms import MultiTopicForm

from django.http import HttpResponse
from django.views.generic import View, TemplateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from braces.views import LoginRequiredMixin

from rest_framework import viewsets
from rest_framework.response import Response
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

        # Compute aggregate statistics via DB query.
        stats = Vote.objects.response_stats()
        context['avg_topics_per_response'] = stats['avg']
        context['min_topics_per_response'] = stats['min']
        context['max_topics_per_response'] = stats['max']

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

class DataDownloadView(LoginRequiredMixin, View):

    queryset = Vote.objects.all()

    def get(self, request):
        """
        Returns a download of the data.
        """
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="topicmaps.csv"'

        # Structures to anonymize IP addresses
        idtag = 0
        ipmap = {}
        dtfmt = "%Y-%m-%d %H:%M"

        # Write CSV to files
        writer = csv.writer(response)
        writer.writerow(('user', 'term', 'time'))
        for vote in self.queryset:
            # Set unique id tag for ip address if not exists
            if vote.ipaddr not in ipmap:
                idtag += 1
                ipmap[vote.ipaddr] = idtag

            # write the row to the CSV file
            writer.writerow([
                ipmap[vote.ipaddr], vote.topic, vote.created.strftime(dtfmt)
            ])

        return response

##########################################################################
## API/DRF Views
##########################################################################

class BadParameter(APIException):

    status_code    = 400
    default_detail = 'Bad parameter passed into GET request.'


class TopicViewSet(viewsets.ViewSet):

    queryset = Topic.objects.with_votes()
    serializer_class = TopicSerializer

    def random_topics(self, limit=10):
        last = Topic.objects.filter(is_canonical=True).count() - 1
        indices = random.sample(xrange(0, last), limit)

        for idx in indices:
            topic = self.queryset[idx]
            yield {
                'title': topic.title,
                'vote_total': int(topic.vote_total),
            }

    def list(self, request):
        try:
            limit    = int(self.request.query_params.get('limit', 300))
            ordering = self.request.query_params.get('ordering', '-vote_total').lower()

            if ordering == 'random':
                return Response(list(self.random_topics(limit)))

            queryset = self.queryset[:limit]
            return Response([
                {
                    'title': topic.title,
                    'vote_total': int(topic.vote_total),
                }
                for topic in queryset
            ])
        except Exception as e:
            raise BadParameter(str(e))


class ResponseViewSet(viewsets.ViewSet):
    """
    Returns statistics and timeseries regarding the responses.
    """

    def list(self, request):
        """
        Returns the time series and other statistics about responses.
        """

        # Compute the time series information
        return Response([
            {'date': d.strftime("%Y-%m-%d"), 'count': c}
            for (d,c) in Vote.objects.response_timeseries()
        ])
