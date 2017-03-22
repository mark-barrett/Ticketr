"""oop3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    # If the user goes to the root directory send them to index (view) #
    url(r'^$', views.index, name='index'),
    # If user goes to event page, include an id to specify the events number #
    url(r'^event/(?P<id>[0-9]+)$', views.event, name='event'),
    url(r'^home/$', views.index, name='index'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^login/$', views.LoginUserFormView.as_view(), name='login'),
    url(r'^create-event/$', views.CreateEventView.as_view(), name='create-view'),
    url(r'^create-organiser/$', views.CreateOrganiserView.as_view(), name='create-organiser'),
    url(r'^organiser-profiles/$', views.OrganiserProfiles.as_view(), name='organiser-profiles'),
    url(r'^organiser/(?P<id>[0-9]+)$', views.organiser, name='organiser'),
    url(r'^my-events/$', views.MyEvents.as_view(), name='my-events'),
    url(r'^manage-event/(?P<id>[0-9]+)$', views.ManageEvent.as_view(), name='manage-event'),
    url(r'^buy-ticket/$', views.BuyTicket.as_view(), name='buy-ticket'),
    url(r'^ticket-timeout/(?P<queue_token>[A-Z]+)$', views.TicketTimeout.as_view(), name='ticket-timeout'),
    url(r'^my-tickets/$', views.MyTickets.as_view(), name='my-tickets'),
    url(r'^download-ticket/(?P<order_number>[0-9]+)$', views.DownloadTicket.as_view(), name='download-ticket')
]
