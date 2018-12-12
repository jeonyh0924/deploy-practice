from django.urls import path

from reservations import apis

urlpatterns_api_tickets = ([
  path('filter/', apis.TicketFilteringView.as_view()),
], 'tickets')