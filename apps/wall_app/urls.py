from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^wall$',views.wall),
    url(r'^sign_up$',views.sign_up),
    url(r'^log_in$',views.log_in),
    url(r'^log_off$',views.log_off),
    url(r'^post_message$',views.post_message),
    url(r'^post_comment/(?P<id>\d+)$',views.post_comment),
    url(r'^comment_delete/(?P<id>\d+)$',views.comment_delete),
    url(r'^message_delete/(?P<id>\d+)$',views.message_delete),
]