from django.conf.urls import url
from . import consumer
websocket_urlpatterns = [
    url(r'^ws/polls/(?P<question_id>[0-9]+)$',
        consumer.PostingConsumer),
]