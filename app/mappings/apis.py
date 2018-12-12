from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from mappings.models import Movie, Theater, Screening
from mappings.serializers import MovieSerializer, MovieDetailSerializer, TheaterListSerializer, \
    TheaterDetailSerializer




# Seat bulk create code

# theater_list = Theater.objects.all()
# auditorium_list = [theater.auditoriums.all() for theater in theater_list]
# for auditorium_set in auditorium_list:
#     for auditorium in auditorium_set:
#         for row in range(1,11):
#             for number in range(1,11):
#                 auditorium.seats.create(row=row, number=number)


# 영화 기본 정보 리스트 API View
# request.GET으로

class MovieListView(APIView):
    def get(self, request):
        if request.GET.get('now_show'):
            movie_list = Movie.objects.filter(now_show=True)
        else:
            movie_list = Movie.objects.all()
        serializers = MovieSerializer(movie_list, many=True, context={"request": request})
        return Response(serializers.data, status=status.HTTP_200_OK)


# now_show false 입력시 상영 예정작 리스트 력
class PreMovieView(APIView):
    def get(self, request):
        movie_list = Movie.objects.filter(now_show=False)
        serializers = MovieSerializer(movie_list, many=True, context={"request": request})
        return Response(serializers.data, status=status.HTTP_200_OK)


# 영화 상세 정보 API View
# 영화 pk를 받는다.
class MovieDetailView(APIView):
    def get(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        serializer = MovieDetailSerializer(movie, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


# 극장 리스트 API View
class TheaterListView(APIView):
    def get(self, request):
        if request.GET.get('location'):
            location = request.GET.get('location')
            theater_list = Theater.objects.filter(location=location)
        else:
            theater_list = Theater.objects.all()
        serializers = TheaterListSerializer(theater_list, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


# 극장 상세 정보 API View
# 극장 pk를 받는다.
class TheaterDetailView(APIView):
    def get(self, request, pk):
        theater = get_object_or_404(Theater, pk=pk)
        serializer = TheaterDetailSerializer(theater, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

