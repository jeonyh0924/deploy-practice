from rest_framework import serializers

from mappings.models import Movie, Stillcut, Cast, Screening, Theater, Auditorium, Seat


class MovieSerializer(serializers.ModelSerializer):
    main_img_url = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        fields = (
            'pk',
            'title',
            'reservation_score',
            'main_img_url',
            'now_show',
            'opening_date'
        )

    def get_main_img_url(self, movie):
        request = self.context.get('request')
        try:
            main_img_url = movie.main_img.url
            return request.build_absolute_uri(main_img_url)
        except AttributeError:
            return ""


class MovieCompactSerializer(serializers.ModelSerializer):
    main_img_url = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = (
            'pk',
            'title',
            'now_show',
            'genre',
            'duration_min',
            'opening_date',
            'main_img_url',
        )

    def get_main_img_url(self, movie):
        request = self.context.get('request')
        try:
            main_img_url = movie.main_img.url
            return request.build_absolute_uri(main_img_url)
        except AttributeError:
            return ""


class StillcutSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Stillcut
        fields = (
            # 'movie',
            'image_url',
        )

    def get_image_url(self, stillcut):
        request = self.context.get('request')
        try:
            image_url = stillcut.image.url
            return request.build_absolute_uri(image_url)
        except AttributeError:
            return ""


class CastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cast
        fields = (
            # 'movie',
            'actor',
        )


class MovieDetailSerializer(serializers.ModelSerializer):
    stillcuts = StillcutSerializer(many=True)
    casts = CastSerializer(many=True)
    main_img_url = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        fields = (
            'pk',
            'title',
            'director',
            'casts',
            'duration_min',
            'opening_date',
            'genre',
            'description',
            'trailer',
            'reservation_score',
            'now_show',
            'main_img_url',
            'stillcuts',
        )

    def get_main_img_url(self, movie):
        request = self.context.get('request')
        try:
            main_img_url = movie.main_img.url
            return request.build_absolute_uri(main_img_url)
        except AttributeError:
            return ""


class AuditoriumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditorium
        fields = (
            'name',
            'seats_no',
        )


# class ScreeningTimeSerializer(serializers.ModelSerializer):
#     current_seats_no = serializers.SerializerMethodField()
#
#     class Meta:
#         model = ScreeningTime
#         fields = (
#             'time',
#             'current_seats_no'
#         )
#
#     def get_current_seats_no(self, screeningtime):
#         auditorium = screeningtime.screening.auditorium
#         return auditorium.seats_no - len(screeningtime.reserved_seats.all())



class ScreeningSerializer(serializers.ModelSerializer):
    auditorium = AuditoriumSerializer()
    current_seats_no = serializers.SerializerMethodField()

    # screening_times = ScreeningTimeSerializer(many=True)

    class Meta:
        model = Screening
        fields = (
            'movie',
            'theater',
            'auditorium',
            'time',
            'current_seats_no'
        )

    def get_current_seats_no(self, screening):
        auditorium = screening.auditorium
        return auditorium.seats_no - len(screening.reserved_seats.all())


class ReservedSeatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screening
        fields = (
            'movie',
            'theater',
            'auditorium',
            'time',
            'reserved_seats'
        )


class TheaterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theater
        fields = (
            'pk',
            'location',
            'sub_location',
        )


class TheaterDetailSerializer(serializers.ModelSerializer):
    current_movies = MovieCompactSerializer(many=True)
    screenings = ScreeningSerializer(many=True)
    all_auditoriums_no = serializers.SerializerMethodField()
    all_seats_no = serializers.SerializerMethodField()

    class Meta:
        model = Theater
        fields = (
            'location',
            'sub_location',
            'address',
            'current_movies',
            'all_auditoriums_no',
            'all_seats_no',
            'screenings'
        )

    def get_all_auditoriums_no(self, theater):
        return len(theater.auditoriums.all())

    def get_all_seats_no(self, theater):
        all_seats_no = 0
        for auditorium in theater.auditoriums.all():
            all_seats_no += auditorium.seats_no
        return all_seats_no


class SeatSeralizer(serializers.ModelSerializer):
    # reservation = serializers.SerializerMethodField()

    class Meta:
        model = Seat
        fields = (
            'row',
            'number',
            # 'auditorium',
            # 'reservation_check'
            # 이걸 메서드 필드로 만고
        )

    def get_reservation_check(self, seat):
        pass


class MovienameSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            'title',
        )