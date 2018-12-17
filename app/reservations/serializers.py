from datetime import datetime

from rest_framework import serializers
from mappings.models import Movie, Theater, Screening, Seat, Reservation
from mappings.serializers import SeatSerializer, ReservedSeatSerializer


# Ticket Movie Serializer


class TicketMovieSerializer(serializers.ModelSerializer):
    show = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = (
            'pk',
            'age',
            'title',
            'show'
        )

    def get_show(self, movie):
        pk_list = self.context.get("show")
        if movie.pk in pk_list:
            return True
        else:
            return False


# Ticket Theater Serializer
class TicketTheaterSubLocationSerializer(serializers.ModelSerializer):
    show = serializers.SerializerMethodField()

    class Meta:
        model = Theater
        fields = (
            'sub_location',
            'show'
        )

    def get_show(self, theater):
        pk_list = self.context.get("show")
        if theater.pk in pk_list:
            return True
        else:
            return False


class TicketTheaterLocationSerializer(serializers.ModelSerializer):
    num = serializers.SerializerMethodField()
    ordering_fields = ('pk',)
    ordering = ('pk',)

    class Meta:
        model = Theater
        fields = (
            'pk',
            'location',
            'num'
        )

    def get_num(self, theater):
        location_pk = Theater.objects.filter(location=theater.location).values_list('pk', flat=True)
        screen_pk = self.context.get("pk_list")
        result_list = [pk for pk in location_pk if pk in screen_pk]
        return len(result_list)

# class TicketTheaterLocationSerializer(serializers.Serializer):
    # location = serializers.CharField(max_length=64)

    # def to_representation(self, instance):
        # data = super(TicketTheaterLocationSerializer, self).to_representation(instance)
        # theater_by_filter = [theater for theater in Theater.objects.all()
        #                      if theater.location == instance["location"]]
        # serializer = TicketTheaterSubLocationSerializer(
        #     theater_by_filter,
        #     many=True,
        #     context={"show": self.context.get("show")}
        # )
        # num = {"num": len(Theater.objects.filter(location=instance["location"]))}
        # return [data, num]
        # return [data, {"theater_set": serializer.data}, num]

# Ticket Screening DateTime Serializer
class TicketScreeningTimeSerializer(serializers.ModelSerializer):
    times = serializers.SerializerMethodField()
    current_seats_no = serializers.SerializerMethodField()

    class Meta:
        model = Screening
        fields = (
            'pk',
            'auditorium',
            'times',
            'current_seats_no'
        )

    def get_times(self, screening):
        return screening.time.time()

    def get_current_seats_no(self, screening):
        auditorium = screening.auditorium
        return auditorium.seats_no - len(screening.reserved_seats.all())


class TicketScreeningDateTimeSerializer(serializers.Serializer):
    date = serializers.CharField()

    # serializer.data 대신 validated_data를 쓴다면 to_internal_value로 데이터를 조작한다.
    # def to_internal_value(self, data):
    #     return data

    # serializer.data 를 쓸 때에만 to_representation을 거쳐간다.
    def to_representation(self, instance):
        if instance["date"] in self.context.get("filter_date_list"):
            show = {"show": True}
        else:
            show = {"show": False}
        data = super(TicketScreeningDateTimeSerializer, self).to_representation(instance)

        # data = super(TicketScreeningDateTimeSerializer, self).to_representation(instance)
        # screening_by_filter = [screen for screen in Screening.objects.all()
        #                        if screen.time.date() == instance["date"] and screen.pk in self.context.get("show")]
        # serializer = TicketScreeningTimeSerializer(screening_by_filter, many=True)
        # if serializer.data:
        #     show = {"show": True}
        # else:
        #     show = {"show": False}
        return [data, show]

class TicketSeatSerializer(serializers.ModelSerializer):
    reservation_check = serializers.SerializerMethodField()

    class Meta:
        model = Seat
        fields = (
            'pk',
            'row',
            'number',
            'seat_name',
            'reservation_check'
        )

    def get_reservation_check(self, seat):
        pk_list = self.context.get("reserved_seats")
        if seat.pk in pk_list:
            return True
        else:
            return False


class TicketReservationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    screening_set = serializers.SerializerMethodField()
    seats_reserved = ReservedSeatSerializer(many=True)
    num = serializers.SerializerMethodField()

    # 여기서 return된 pk는 "예매번호" 로 사용할 수 있도록 한다.
    class Meta:
        model = Reservation
        fields = (
            'pk',
            'user',
            'screening_set',
            'num',
            'seats_reserved',
            'is_active',
        )
        read_only_fields = (
            'user',
        )

    def get_screening_set(self, reservation):
        request = self.context.get("request")
        screen = reservation.screening
        movie = screen.movie
        try:
            img_url = request.build_absolute_uri(movie.main_img.url)
            thumb_img_url = request.build_absolute_uri(movie.thumbnail_img.url)
        except AttributeError:
            img_url = ""
            thumb_img_url = ""
        title = movie.title
        age = movie.age
        theater = screen.theater.sub_location
        time = datetime.strftime(screen.time, "%Y-%m-%d %H:%M")
        return {
            "img_url": img_url,
            "thumb_img_url": thumb_img_url,
            "title": title,
            "age": age,
            "theater": theater,
            "time": time
        }

    def get_num(self, reservation):
        return len(reservation.seats_reserved.all())
