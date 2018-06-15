from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^create_message/$', views.create_message),
    url(r'^edit_task/(?P<id>\d+)$', views.edit_task, name='edit'),
    url(r'^create_task/$', views.create_task), 
    url(r'^view_task/(?P<id>\d+)$', views.view_task), 
    url(r'^remove_task/(?P<id>\d+)$', views.remove_task), 
    url(r'^claim_task/(?P<id>\d+)$', views.add_task, name='claim-a-task'), 
    url(r'^view_person/(?P<id>\d+)$', views.view_person, name='view-person'),
    url(r'^view_profile/(?P<id>\d+)$', views.view_profile, name='view-profile'),
    url(r'^add_friend/(?P<id>\d+)$', views.add_friend, name='add-friend'),
    url(r'^remove_friend/(?P<id>\d+)$', views.remove_friend, name='remove-friend'),
    url(r'^process/$', views.create),   
    url(r'^logout/$', views.logout),   
    url(r'^login/$', views.login),   
    url(r'^user_home/$', views.user_home),   
    url(r'^$', views.index),   
] 