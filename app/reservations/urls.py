from django.urls import path

from reservations import apis

urlpatterns_api_tickets = ([
  path('filter/', apis.TicketFilteringView.as_view()),
  path('select-seats/<int:pk>/', apis.ReservedSeatsList.as_view()),
], 'tickets')