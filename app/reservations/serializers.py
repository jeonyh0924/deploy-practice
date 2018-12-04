from rest_framework import serializers

from reservations.models import Movie, Stillcut, Cast


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

        # fields = '__all__'
    # def get_main_img_url(self, movie):
    #     request = self.context.get('request')
    #     main_img_url = movie.main_img.url
    #     return request.build_absolute_uri(main_img_url)
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
