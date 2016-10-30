from django.conf.urls import url
from django.views.generic.base import TemplateView
from .views import login_view, logout_view, register_view, TopicNewest, TopicActive, TopicList, TopicView, TopicAPI, TopicVoteAPI, PostAPI, PostVoteAPI

urlpatterns = [
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^register/$', register_view, name='register'),

    url(r'^$', TopicNewest.as_view(), name='topic_list'),
    url(r'^active/$', TopicActive.as_view(), name='topic_active'),
    url(r'^(?P<slug>[\w-]+)/$', TopicList.as_view(), name='topic_list_cat'),
    url(r'^topic/(?P<slug>[\w_-]+)/$', TopicView.as_view(), name='topic_view'),

    url(r'^api/topic/$', TopicAPI.as_view(), name='topic_api'),
    url(r'^api/topic/vote/$', TopicVoteAPI.as_view(), name='topic_vote_api'),
    url(r'^api/post/$', PostAPI.as_view(), name='post_api'),
    url(r'^api/post/vote/$', PostVoteAPI.as_view(), name='post_vote_api'),
]
