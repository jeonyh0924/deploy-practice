import pytz
from django.conf import settings
from django.utils import timezone
from rest_framework import serializers

from mappings.models import Movie, Theater, Screening


class TicketMovieSerializer(serializers.ModelSerializer):
    selected = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = (
            'pk',
            'title',
            'selected'
        )

    def get_selected(self, movie):
        pk_list = self.context.get("selected")
        if movie.pk in pk_list:
            return True
        else:
            return False


class TicketTheaterSerializer(serializers.ModelSerializer):
    selected = serializers.SerializerMethodField()

    class Meta:
        model = Theater
        fields = (
            'pk',
            'location',
            'sub_location',
            'selected'
        )

    def get_selected(self, theater):
        pk_list = self.context.get("selected")
        if theater.pk in pk_list:
            return True
        else:
            return False

class TicketScreeningDateSerializer(serializers.ModelSerializer):
    selected = serializers.SerializerMethodField()

    class Meta:
        model = Screening
        fields = (
            'pk',
            'time',
            'selected'
        )

    def get_selected(self, screening):
        pk_list = self.context.get("selected")
        if screening.pk in pk_list:
            return True
        else:
            return False

# class TicketDatetimeSerializer(serializers.Serializer):
#     date = serializers.DateTimeField()



# class TicketFilterSerializer(serializers.Serializer):
#     def get_movie_list(self):
#         movie_list = self.context.get('movie_list')
#         return movie_list
#
#     def get_theater_list(self):
#         theater_list = self.context.get('theater_list')
#         return theater_list
#
#     def get_date_list(self):
#         date_list = self.context.get('date_list')
#         return date_list
#
#     movie_list = TicketMovieSerializer(get_movie_list, many=True)
#     theater_list = TicketTheaterSerializer(get_theater_list, many=True)
#     date_list = TicketDatetimeSerializer(get_date_list, many=True)
