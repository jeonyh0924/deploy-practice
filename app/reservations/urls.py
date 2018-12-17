from django.urls import path

from reservations import apis

urlpatterns_api_tickets = ([
    path('filter/', apis.TicketFilteringView.as_view()),
    path('seats/<int:pk>/', apis.TicketSeatListView.as_view()),
    path('reservations/', apis.TicketReservationView.as_view()),
    path('m/movies/', apis.AppTicketMovieListView.as_view()),
    path('m/filter/<int:pk>/', apis.AppTicketFilteringView.as_view()),
    path('m/seats/<int:pk>/', apis.TicketSeatListView.as_view()),
    path('m/reservations/', apis.TicketReservationView.as_view()),
], 'tickets')