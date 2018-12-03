from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from reservations.models import Movie
from reservations.serializers import MovieSerializer, MovieDetailSerializer

# 영화 기본 정보 리스트 API View


class MovieListView(APIView):
    def get(self, request):
        movie_list = Movie.objects.all()
        serializers = MovieSerializer(movie_list, many=True, context={"request": request})
        return Response(serializers.data)


# 영화 상세 정보 리스트 API View
# 영화 pk를 받는다.
class MovieDetailView(APIView):
    def get(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        serializer = MovieDetailSerializer(instance=movie, context={"request": request})
        return Response(serializer.data)
