from django.urls import path

from reservations import apis

urlpatterns_api_tickets = ([
    path('filter/', apis.TicketFilteringView.as_view()),
    path('seats/<int:pk>/', apis.TicketSeatListView.as_view()),
    path('reservations/', apis.TicketReservationView.as_view()),
], 'tickets')