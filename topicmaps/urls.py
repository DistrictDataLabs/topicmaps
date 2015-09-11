# topicmaps.urls
# Application url definition and routers.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Aug 21 13:21:31 2015 -0500
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: urls.py [] benjamin@bengfort.com $

"""
Application url definition and routers.
"""

##########################################################################
## Imports
##########################################################################

from django.contrib import admin
from rest_framework import routers
from django.conf.urls import include, url

from django.views.generic import TemplateView

from topicmaps.views import *
from topics.views import *

##########################################################################
## Endpoint Discovery
##########################################################################

## API
router = routers.DefaultRouter()
router.register(r'status', HeartbeatViewSet, "status")
router.register(r'topics', TopicViewSet, "topic")
router.register(r'responses', ResponseViewSet, "response")

##########################################################################
## URL Patterns
##########################################################################

urlpatterns = [
    # Admin URLs
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Application URLs
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^survey/$', MultiTopicView.as_view(), name='survey'),
    url(r'^results/$', ResultView.as_view(), name='results'),
    url(r'^terms/$', TemplateView.as_view(template_name='site/legal/terms.html'), name='terms'),
    url(r'^privacy/$', TemplateView.as_view(template_name='site/legal/privacy.html'), name='privacy'),

    # Authentication URLs
    url('^accounts/', include('django.contrib.auth.urls')),

    ## REST API Urls
    url(r'^api/', include(router.urls, namespace="api")),
]
