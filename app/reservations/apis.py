from datetime import datetime
import pytz
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


# 예매 프로세스
# 예매 필터링 API View
from mappings.models import Screening, Movie, Theater
from reservations.serializers import TicketMovieSerializer, TicketTheaterSerializer, TicketScreeningDateSerializer


class TicketFilteringView(APIView):
    def movie_filter(self, request):
        if request.GET.get('movie') is not None:
            movie = request.GET.get('movie')
            return Q(movie__title=movie)
        else:
            return Q(movie__isnull=False)

    def location_filter(self, request):
        if request.GET.get('location') is not None:
            location = request.GET.get('location')
            return Q(theater__location=location)
        else:
            return Q(theater__location__isnull=False)

    def sub_location_filter(self, request):
        if request.GET.get('sub_location') is not None:
            sub_location = request.GET.get('sub_location')
            return Q(theater__sub_location=sub_location)
        else:
            return Q(theater__sub_location__isnull=False)

    def time_filter(self, request):
        if request.GET.get('time') is not None:
            raw_time = request.GET.get('time') + ' 00:00:00'
            base_time = datetime.strptime(raw_time, '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.UTC)
            max_time = (base_time + datetime.timedelta(hours=23, minutes=59, seconds=59)).replace(tzinfo=pytz.UTC)

            return Q(time__gt=base_time) & Q(time__lt=max_time)
        else:
            return Q(time__isnull=False)

    def get(self, request):
        context = {}

        screens = Screening.objects.filter(self.movie_filter(request) & self.location_filter(request) & self.sub_location_filter(request) & self.time_filter(request))

        # movie_list = [screen.movie for screen in screens]
        movie_pk_list = [screen.movie.pk for screen in screens]
        all_movie_list = Movie.objects.all()
        # theater_list = [screen.theater for screen in screens]
        theater_pk_list = [screen.theater.pk for screen in screens]
        all_theater_list = Theater.objects.all()
        # time_list = [screen.time for screen in screens]
        # date_list = [{'date': time} for time in time_list]
        screening_pk_list = [screen.pk for screen in screens]
        all_screening_list = Screening.objects.all()

        movie_serializer = TicketMovieSerializer(
            all_movie_list,
            context={"selected": movie_pk_list},
            many=True
        )
        context["movie"] = movie_serializer.data

        theater_serializer = TicketTheaterSerializer(
            all_theater_list,
            context={"selected": theater_pk_list},
            many=True
        )
        context["theater"] = theater_serializer.data

        date_serializer = TicketScreeningDateSerializer(
            all_screening_list,
            context={"selected": screening_pk_list},
            many=True
        )
        context["date"] = date_serializer.data
        # date_serializer = TicketScreeningDateSerializer(data=date_list, many=True)
            # context["date"] = date_serializer.validated_data
        return Response(context, status=status.HTTP_200_OK)

