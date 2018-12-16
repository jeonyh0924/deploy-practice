# import datetime
# from datetime import date
import datetime
import operator

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
    TicketTheaterLocationSerializer, TicketSeatSerializer, TicketReservationSerializer, \
    TicketTheaterSubLocationSerializer, TicketScreeningTimeSerializer


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
            base_time = datetime.datetime.strptime(raw_time, '%Y-%m-%d %H:%M:%S')
            # .replace(tzinfo=pytz.UTC)
            max_time = base_time + datetime.timedelta(hours=23, minutes=59, seconds=59)
            # .replace(tzinfo=pytz.UTC)

            return Q(time__gt=base_time) & Q(time__lt=max_time)
        else:
            return Q(time__isnull=False)

    def get(self, request):
        context = {}
        screens = Screening.objects.filter(self.movie_filter(request) & self.location_filter(request) & self.sub_location_filter(request) & self.time_filter(request))

        # Movie serializer
        filter_movie_pk_list = [screen.movie.pk for screen in screens]

        movie_serializer = TicketMovieSerializer(
            Movie.objects.order_by('-reservation_score'),
            context={"show": filter_movie_pk_list},
            many=True
        )
        context["movie"] = movie_serializer.data

        # Theater serializer
        # location_list = Theater.objects.values_list('location', flat=True).distinct()
        # location_dict = []
        # for location in location_list:
        #     location_element = {"location": location}
        #     location_dict.append(location_element)
        filter_theater_pk_list = list(set([screen.theater.pk for screen in screens]))

        location_serializer = TicketTheaterLocationSerializer(
            sorted(Theater.objects.order_by('location').distinct('location'), key=operator.attrgetter('pk')),
            context={"pk_list": filter_theater_pk_list},
            many=True
        )
        # context = {"show": filter_theater_pk_list},
        # if location_serializer.is_valid():
        context["location"] = location_serializer.data

        if request.GET.get('location') is not None:
            location = request.GET.get('location')
            # filter_theater_pk_list = list(
            #     set([screen.theater.pk for screen in screens.filter(theater__location=location)]))
            sub_location_serializer = TicketTheaterSubLocationSerializer(
                Theater.objects.filter(location=location),
                context={"show": filter_theater_pk_list},
                many=True
            )
            context["sub_location"] = sub_location_serializer.data


        # DateTime serializer
        start = datetime.datetime.today()
        end = start + datetime.timedelta(days=14)
        date_set = [datetime.datetime.strftime((start + datetime.timedelta(days=x)), "%Y-%m-%d") for x in range(0, (end - start).days)]
        date_list = []
        for date in date_set:
            date_dict = {"date": date}
            date_list.append(date_dict)

        filter_date_list = list(set([datetime.datetime.strftime(screen.time, "%Y-%m-%d") for screen in screens]))
        # filter_date_list = []
        # for date in filter_date_set:
        #     date_dict = {"date": date}
        #     filter_date_list.append(date_dict)

        date_serializer = TicketScreeningDateTimeSerializer(
            data=date_list,
            many=True,
            context={"filter_date_list": filter_date_list}
        )
        if date_serializer.is_valid():
            context["date"] = date_serializer.data


        if request.GET.get('location') is not None and request.GET.get('sub_location') is not None and request.GET.get('time') is not None and request.GET.get('movie') is not None:
            serializer = TicketScreeningTimeSerializer(
                screens, many=True
            )
            context["time"] = serializer.data

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