from django.urls import path
from . import apis

urlpatterns_api_movies = ([
  path('list/', apis.MovieListView.as_view()),
  path('detail/<int:pk>/', apis.MovieDetailView.as_view()),
], 'movies')

urlpatterns_api_theaters = ([
  path('list/', apis.TheaterListView.as_view()),
  path('detail/<int:pk>/', apis.TheaterDetailView.as_view()),
], 'theaters')