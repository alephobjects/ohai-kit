from django.conf.urls import patterns, url
from ohai_kit import views


urlpatterns = patterns(
    '',
    url(r'^$', views.system_index, name='index'),
    url(r'^group/$', views.ungrouped_view, name='misc_group'),
    url(r'^group/(?P<group_id>\d+)/$', views.group_view, name='named_group'),
    url(r'^workflow/(?P<project_slug>\w+)/$', views.project_view, name='project'),
    url(r'^workflow/(?P<project_slug>\w+)/start/$', 
        views.start_job, name='start_job'),

    url(r'^jobs/(?P<job_id>\d+)/$', views.job_status, name='job_status'),
    url(r'^jobs/(?P<job_id>\d+)/close$', views.close_job, name='close_job'),
    url(r'^jobs/(?P<job_id>\d+)/update$', views.update_job, name='update_job'),

    url(r'^session_settings/$', views.session_settings, name='session_settings'),

    url(r'^project/(?P<project_slug>\w+)/$', views.guest_workflow, name='guest_workflow'),
    url(r'accounts/guest_bypass/$', views.guest_access, name='guest_access'),

    url(r'^accounts/login/$', views.worker_access, 
        {'template_name': 'ohai_kit/login.html',
         'extra_context':{'touch_emulation':False}}, name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', 
        {'next_page': '/'}),
)
