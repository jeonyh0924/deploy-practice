# import datetime
# from datetime import date
import datetime
import pytz
from django.db import transaction, IntegrityError
from django.db.models import Q
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView


# 예매 프로세스
# 예매 필터링 API View
from mappings.models import Screening, Movie, Theater, ReservedSeat, Seat, Reservation
from reservations.serializers import TicketMovieSerializer, TicketScreeningDateTimeSerializer, \
    TicketTheaterLocationSerializer, TicketSeatSerializer, TicketReservationSerializer


class TicketFilteringView(APIView):
    # permission_classes = (
    #     permissions.IsAuthenticated,
    # )
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
        elif request.GET.get('sub_location') is not None:
            sub_location = request.GET.get('sub_location')
            theater = Theater.objects.get(sub_location=sub_location)
            location = theater.location
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
            base_time = datetime.datetime.strptime(raw_time, '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.UTC)
            max_time = (base_time + datetime.timedelta(hours=23, minutes=59, seconds=59)).replace(tzinfo=pytz.UTC)

            return Q(time__gt=base_time) & Q(time__lt=max_time)
        else:
            return Q(time__isnull=False)

    def get(self, request):
        context = {}
        screens = Screening.objects.filter(self.movie_filter(request) & self.location_filter(request) & self.sub_location_filter(request) & self.time_filter(request))

        # Movie serializer
        filter_movie_pk_list = [screen.movie.pk for screen in screens]

        movie_serializer = TicketMovieSerializer(
            Movie.objects.all(),
            context={"show": filter_movie_pk_list},
            many=True
        )
        context["movie"] = movie_serializer.data

        # Theater serializer
        filter_theater_pk_list = list(set([screen.theater.pk for screen in screens]))
        location_set = list(set(theater.location for theater in Theater.objects.all()))
        location_list = []
        for location in location_set:
            location_dict = {"location": location}
            location_list.append(location_dict)

        location_serializer = TicketTheaterLocationSerializer(
            data=location_list,
            context={"show": filter_theater_pk_list},
            many=True
        )
        if location_serializer.is_valid():
            context["theater"] = location_serializer.data

        # DateTime serializer
        filter_screening_pk_list = [screen.pk for screen in screens]
        date_set = list(set([screen.time.date() for screen in Screening.objects.all()]))
        date_list = []
        for date in date_set:
            date_dict = {"date": date}
            date_list.append(date_dict)

        date_serializer = TicketScreeningDateTimeSerializer(
            data=date_list,
            many=True,
            context={"show": filter_screening_pk_list}
        )
        if date_serializer.is_valid():
            context["date"] = date_serializer.data

        return Response(context, status=status.HTTP_200_OK)


class TicketSeatListView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request, pk):
        screen = Screening.objects.get(pk=pk)
        auditorium = screen.auditorium
        reserved_pk_list = [seat.pk for seat in screen.reserved_seats.all()]
        serializer = TicketSeatSerializer(auditorium.seats.all(), many=True, context={"reserved_seats": reserved_pk_list})
        return Response(serializer.data, status=status.HTTP_200_OK)


class TicketReservationView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request):
        try:
            with transaction.atomic():
                screen = Screening.objects.get(pk=request.GET.get("screen"))
                selected_seats_pk = request.GET.get("seats")
                for pk in selected_seats_pk:
                    if pk in [seat.pk for seat in screen.reserved_seats.all()]:
                        return Response({"message": "이미 예약된 좌석입니다. 다른 좌석을 선택해 주세요."},
                                        status=status.HTTP_400_BAD_REQUEST)

                reservation = Reservation.objects.create(
                    user=request.user,
                    screening=screen,
                )

                for seat_pk in selected_seats_pk:
                    ReservedSeat.objects.create(
                        screening=screen,
                        seat=Seat.objects.get(pk=seat_pk),
                        reservation=reservation
                    )

                serializer = TicketReservationSerializer(reservation, context={"request": request})
                return Response(serializer.data, status=status.HTTP_200_OK)
        except IntegrityError:
            return Response({"message": "이미 예약된 좌석입니다. 다른 좌석을 선택해 주세요."}, status=status.HTTP_400_BAD_REQUEST)