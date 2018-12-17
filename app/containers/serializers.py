from rest_framework import serializers

from containers.models import WebTrailerContainer, AppTrailerContainer, MainContainer
from mappings.models import Movie


class MainContainerSerializer(serializers.ModelSerializer):
    container_img_url = serializers.SerializerMethodField()

    class Meta:
        model = MainContainer
        fields = (
            'event_name',
            'container_img_url',
            'container_link'
        )

    def get_container_img_url(self, container):
        request = self.context.get("request")
        try:
            container_img_url = container.container_img.url
            return request.build_absolute_uri(container_img_url)
        except AttributeError:
            return ""



class WebTrailerSerializer(serializers.ModelSerializer):
    movie_title = serializers.SerializerMethodField()
    movie_trailer = serializers.SerializerMethodField()
    posting_img_url = serializers.SerializerMethodField()

    class Meta:
        model = WebTrailerContainer
        fields = (
            'movie_title',
            'movie_trailer',
            'posting_img_url'
        )

    def get_movie_title(self, container):
        return container.movie.title

    def get_movie_trailer(self, container):
        return container.movie.trailer

    def get_posting_img_url(self, container):
        request = self.context.get("request")
        try:
            posting_img_url = container.posting_img.url
            return request.build_absolute_uri(posting_img_url)
        except AttributeError:
            return ""


class AppTrailerSerializer(serializers.ModelSerializer):
    movie_pk = serializers.SerializerMethodField()
    movie_title = serializers.SerializerMethodField()
    movie_trailer = serializers.SerializerMethodField()
    posting_img_url = serializers.SerializerMethodField()

    class Meta:
        model = AppTrailerContainer
        fields = (
            'movie_pk',
            'movie_title',
            'movie_trailer',
            'comment',
            'posting_img_url'
        )

    def get_movie_pk(self, container):
        return container.movie.pk

    def get_movie_title(self, container):
        return container.movie.title

    def get_movie_trailer(self, container):
        return container.movie.trailer

    def get_posting_img_url(self, container):
        request = self.context.get("request")
        try:
            posting_img_url = container.posting_img.url
            return request.build_absolute_uri(posting_img_url)
        except AttributeError:
            return ""


class EventContainerSerializer(serializers.ModelSerializer):
    container_img_url = serializers.SerializerMethodField()

    class Meta:
        model = MainContainer
        fields = (
            'event_name',
            'container_img_url',
            'container_link'
        )

    def get_container_img_url(self, container):
        request = self.context.get("request")
        try:
            container_img_url = container.container_img.url
            return request.build_absolute_uri(container_img_url)
        except AttributeError:
            return ""


class EventFooterContainerSerializer(serializers.ModelSerializer):
    container_img_url = serializers.SerializerMethodField()

    class Meta:
        model = MainContainer
        fields = (
            'event_name',
            'container_img_url',
            'container_link'
        )

    def get_container_img_url(self, container):
        request = self.context.get("request")
        try:
            container_img_url = container.container_img.url
            return request.build_absolute_uri(container_img_url)
        except AttributeError:
            return ""
