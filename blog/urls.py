from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/like_comment/$', views.like_comment, name='like_comment'),
    url(r'^post/comment/$', views.comment, name='comment'),
    url(r'^post/load_comment/$', views.load_comment, name='load_comment'),
    # url(r'^post/create/$', views.create_comment, name='create_comment'),
]
