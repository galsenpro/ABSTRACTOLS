#-*- coding: utf-8 -*-
from abstract import views
from django.conf.urls import include, url
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
import notifications.urls
urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^$', views.home),
    url(r'^admin/', include(admin.site.urls)),
   # url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    #url(r'^email_confirmation/', include('email_confirm_la.urls', namespace='email_confirm_la')),
]
# Change admin site title
#admin.site.site_header = _("ABSTRACT")
#admin.site.site_title = _("ABSTRACT")
