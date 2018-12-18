import random

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from containers.models import *
from containers.serializers import MainContainerSerializer, WebTrailerSerializer, AppTrailerSerializer
from mappings.serializers import MovieSerializer


class WebHomeView(APIView):
    def get(self, request):
        context = {"request": request}
        try:
            main_serializers = MainContainerSerializer(MainContainer.objects.filter(is_active=True), many=True, context=context)
            main_data = main_serializers.data
        except ObjectDoesNotExist:
            main_data = ""

        try:
            event_serializers = MainContainerSerializer(EventContainer.objects.filter(is_active=True), many=True, context=context)
            event_data = event_serializers.data
        except ObjectDoesNotExist:
            event_data = ""

        try:
            footer_serializers = MainContainerSerializer(EventFooterContainer.objects.filter(is_active=True)[0], context=context)
            footer_data = footer_serializers.data
        except IndexError:
            footer_data = ""
        try:
            web_serializer = WebTrailerSerializer(random.choice(WebTrailerContainer.objects.all()), context=context)
            web_data = web_serializer.data
        except IndexError:
            web_data = ""

        return Response(
            {
                "main_container": main_data,
                "trailer": web_data,
                "event_container": event_data,
                "footer_container": footer_data,
            }, status=status.HTTP_200_OK)


class AppHomeView(APIView):
    def get(self, request):
        context = {"request": request}
        try:
            main_serializers = MainContainerSerializer(MainContainer.objects.filter(is_active=True), many=True,
                                                       context=context)
            main_data = main_serializers.data
        except ObjectDoesNotExist:
            main_data = ""

        try:
            event_serializers = MainContainerSerializer(EventContainer.objects.filter(is_active=True), many=True,
                                                        context=context)
            event_data = event_serializers.data
        except ObjectDoesNotExist:
            event_data = ""

        try:
            footer_serializers = MainContainerSerializer(EventFooterContainer.objects.filter(is_active=True)[0],
                                                         context=context)
            footer_data = footer_serializers.data
        except IndexError:
            footer_data = ""
        try:
            app_serializer = AppTrailerSerializer(random.choice(AppTrailerContainer.objects.all()), context=context)
            app_data = app_serializer.data
        except IndexError:
            app_data = ""

        if request.data.get("now_open"):
            chart_list = Movie.objects.order_by('-reservation_score').filter(now_open=True)
        else:
            chart_list = Movie.objects.order_by('opening_date').filter(now_open=False)

        serializer = MovieSerializer(
            chart_list,
            many=True,
            context=context
        )
        return Response(
            {
                "main_container": main_data,
                "trailer": app_data,
                "event_container": event_data,
                "footer_container": footer_data,
                "chart": serializer.data
            }, status=status.HTTP_200_OK)