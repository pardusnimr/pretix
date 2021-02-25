from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/sendmail/$', views.SenderView.as_view(),
        name='send'),
    url(r'^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/sendmail/history/', views.EmailHistoryView.as_view(),
        name='history'),
    url(r'^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/sendmail/rules/create', views.CreateRule.as_view(),
        name='rule.create'),
    url(r'^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/sendmail/rules/(?P<rule>[^/]+)/delete', views.DeleteRule.as_view(),
        name='rule.delete'),
    url(r'^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/sendmail/rules/(?P<rule>[^/]+)', views.UpdateRule.as_view(),
        name='rule.update'),
    url(r'^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/sendmail/rules', views.ListRules.as_view(),
        name='rule.list'),
]
