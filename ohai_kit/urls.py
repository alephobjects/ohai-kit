from django.conf.urls import patterns, url
from ohai_kit import views


urlpatterns = patterns(
    '',
    url(r'^$', views.system_index, name='index'),
    url(r'^project/(?P<project_id>\d+)/$', views.project_view, name='project'),
    url(r'^project/(?P<project_id>\d+)/start$', 
        views.start_job, name='start_job'),

    url(r'^jobs/(?P<job_id>\d+)/$', views.job_status, name='job_status'),
    url(r'^jobs/(?P<job_id>\d+)/close$', views.close_job, name='close_job'),
    url(r'^jobs/(?P<job_id>\d+)/update$', views.update_job, name='update_job'),

    url(r'^guest_workflow/(?P<project_id>\d+)/$', views.guest_workflow, name='guest_workflow'),
    url(r'accounts/guest_bypass/$', views.guest_access, name='guest_access'),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', 
        {'template_name': 'ohai_kit/login.html'}, name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', 
        {'next_page': '/'}),
)
