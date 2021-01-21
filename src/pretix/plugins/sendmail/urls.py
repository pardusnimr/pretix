from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/sendmail/$', views.SenderView.as_view(),
        name='send'),
    url(r'^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/sendmail/history/', views.EmailHistoryView.as_view(),
        name='history'),
    url(r'^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/sendmail/schedule', views.CreateRule.as_view(),
        name='schedule'),
    url(r'^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/sendmail/rules', views.ListRules.as_view(),
        name='listrules'),
    url(r'^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/sendmail/(?P<rule>[^/]+)', views.UpdateRule.as_view(),
        name='updaterule'),
]
