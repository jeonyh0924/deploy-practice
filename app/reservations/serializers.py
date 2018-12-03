from rest_framework import serializers

from reservations.models import Movie, Stillcut


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

    def get_main_img_url(self, movie):
        request = self.context.get('request')
        main_img_url = movie.main_img.url
        return request.build_absolute_uri(main_img_url)


class StillcutSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Stillcut
        fields = (
            'movie',
            'image_url',
        )

    def get_image_url(self, stillcut):
        request = self.context.get('request')
        image_url = stillcut.image.url
        return request.build_absolute_uri(image_url)


class MovieDetailSerializer(serializers.ModelSerializer):
    stillcuts = StillcutSerializer(many=True)
    main_image_url = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        fields = (
            'pk',
            'title',
            'director',
            'cast',
            'duration_min',
            'opening_date',
            'genre',
            'description',
            'trailer',
            'reservation_score',
            'now_show',
            'main_image_url',
            'stillcuts',
        )

    def get_main_image_url(self, movie):
        request = self.context.get('request')
        main_image_url = movie.main_image.url
        return request.build_absolute_uri(main_image_url)