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
    url(r'^download-ticket/(?P<order_number>[0-9]+)$', views.DownloadTicket.as_view(), name='download-ticket'),
    url(r'^manage-event/orders/?(?P<id>[\w]+)?/?(?P<ticket_id>[0-9]+)?/$', views.EventViewOrders.as_view(), name='view-orders-event'),
    url(r'^manage-event/tickets/(?P<id>[0-9]+)$', views.EventViewTickets.as_view(), name='view-tickets-event'),
    url(r'^manage-event/tickets/(?P<id>[0-9]+)/add$', views.EventAddTicket.as_view(), name='add-ticket-event'),
    url(r'^manage-event/tickets/(?P<id>[0-9]+)/delete/(?P<ticket_id>[0-9]+)$', views.EventDeleteTicket.as_view(), name='delete-ticket-event'),
    url(r'^view-order/(?P<id>[0-9]+)$', views.ViewOrder.as_view(), name='view-order'),
    url(r'^resell-ticket/(?P<order_id>[0-9]+)$', views.ResellTicket.as_view(), name='resell-ticket'),
    url(r'^sell-ticket/$', views.SellTicket.as_view(), name='sell-ticket'),
    url(r'^manage-event/discount-codes/(?P<id>[0-9]+)$', views.DiscountCodes.as_view(), name='discount-codes'),
    url(r'^manage-event/discount-codes/(?P<id>[0-9]+)/add$', views.DiscountCodesAdd.as_view(), name='discount-codes-add')
]
