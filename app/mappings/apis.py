# import string

# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from mappings.models import Movie, Theater
from mappings.serializers import MovieSerializer, MovieDetailSerializer, TheaterListSerializer, \
    TheaterDetailSerializer, MovieOfficialListSerializer


# Seat bulk create code
# alphabet = string.ascii_uppercase
#
# theater_list = Theater.objects.all()
# auditorium_list = [theater.auditoriums.all() for theater in theater_list]
# for auditorium_set in auditorium_list:
#     for auditorium in auditorium_set:
#         for row in range(1,11):
#             for number in range(1,11):
#                 auditorium.seats.create(row=row, number=number, seat_name=f'{alphabet[row-1]}' + f'{number}')


# 영화 기본 정보 리스트 API View
# now_show를 받아야함
# GET으로 page를 보내줘야함
# class MovieListView(APIView):
#     def get(self, request):
#         if request.GET.get('now_show'):
#             movie_list = Movie.objects.filter(now_show=True)
#         else:
#             movie_list = Movie.objects.all()
#
#         paginator = Paginator(movie_list, 8)
#         page = request.GET.get('page')
#         try:
#             page_movie_list = paginator.page(page)
#         except PageNotAnInteger:
#             page_movie_list = paginator.page(1)
#         except EmptyPage:
#             page_movie_list = paginator.page(paginator.num_pages)
#
#         serializers = MovieSerializer(page_movie_list, many=True, context={"request": request})
#         return Response(serializers.data, status=status.HTTP_200_OK)


class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.order_by('-reservation_score')
    serializer_class = MovieSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        if self.request.GET.get('now_show'):
            query_set = Movie.objects.filter(now_show=True)
        else:
            query_set = super(MovieListView, self).get_queryset()
        return query_set


# now_show false 입력시 상영 예정작 리스트 출력
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
# 지역이 주어지면 해당 지역의 극장이 선택된다
# 지역을 받지 못한 경우 모든 극장이 리턴
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


class MovieOfficialListView(APIView):
    def get(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        serializer = MovieOfficialListSerializer(movie, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
