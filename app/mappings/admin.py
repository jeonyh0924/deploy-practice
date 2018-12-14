import datetime

from django.contrib import admin
import nested_admin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.utils import timezone
from nested_admin.nested import NestedModelAdmin
from mappings.models import *


# 좌석 bulk create 기능 가능 여부
# image 프리뷰 달기
# custom button & custom View 생성 여부 > 영화 검색기능 달기(영화진흥위원회 Open API 활용)
# 관리자 기능 마무리되면 admin page 템플릿 조정


# 영화 Admin setting
class StillcutInline(nested_admin.nested.NestedStackedInline):
    model = Stillcut
    extra = 1


class CastingInline(nested_admin.nested.NestedStackedInline):
    model = Casting
    extra = 1


class DirectingInline(nested_admin.nested.NestedStackedInline):
    model = Directing
    extra = 1


class MovieAdmin(nested_admin.nested.NestedModelAdmin):
    def now_open_update(modeladmin, request, queryset):
        for movie in queryset:
            if movie.opening_date <= datetime.date.today():
                movie.now_open = True
                movie.save()

    def now_show_update(modeladmin, request, queryset):
        for movie in queryset:
            if movie.screenings.first():
                movie.now_show = True
                movie.save()
            else:
                movie.now_show = False
                movie.save()

    now_open_update.short_description = "현재 개봉작 업데이트"
    now_show_update.short_description = "현재 상영작 업데이트"

    list_display = ['title']
    list_filter = (
        'genre',
        'now_open',
        'now_show',
    )
    inlines = [DirectingInline, CastingInline, StillcutInline]
    actions = [now_show_update, now_open_update]

    def save_model(self, request, obj, form, change):
        super(MovieAdmin, self).save_model(request, obj, form, change)
        for file in request.FILES.getlist('photos_multiple'):
            obj.images.create(file=file)


# 상영 Admin setting
# class ScreeningTimeInline(nested_admin.nested.NestedTabularInline):
#     model = ScreeningTime
#     extra = 1


# class ScreeningAdmin(nested_admin.nested.NestedModelAdmin):
#     inlines = [ScreeningTimeInline]


# 상영관 Admin setting
class ScreeningInline(nested_admin.nested.NestedStackedInline):
    model = Screening
    extra = 1
    ordering = ('-time',)

class SeatInline(nested_admin.nested.NestedTabularInline):
    model = Seat
    extra = 1


# 상영관 Admin setting
class AuditoriumAdmin(nested_admin.nested.NestedModelAdmin):
    inlines = [ScreeningInline, SeatInline]
    list_display = ('name', 'theater', 'seats_no', 'get_movie')
    list_filter = (
        'theater__location',
        'theater__sub_location',
                   )

    def get_movie(self, obj):
        screening = obj.screenings.first()
        return screening


class AuditoriumInline(nested_admin.nested.NestedStackedInline):
    model = Auditorium
    extra = 1

#
# class CurrentMovieInline(nested_admin.nested.NestedStackedInline):
#     model = Theater.current_movies.through


# 극장 admin setting
class TheaterAdmin(nested_admin.nested.NestedModelAdmin):
    model = Theater
    inlines = [AuditoriumInline]
    list_display = ('sub_location', 'location', 'get_auditorium')
    list_filter = (
        'location',
        'current_movies',
    )

    def get_auditorium(self, obj):
        auditoriums = obj.auditoriums.all()
        return [auditorium for auditorium in auditoriums]


class ReservationAdmin(admin.ModelAdmin):
    model = Reservation
    list_display = ('user', 'get_movie', 'get_theater', 'get_seat', 'is_active')

    def get_movie(self, obj):
        return obj.screening.movie

    def get_theater(self, obj):
        return obj.screening.theater

    def get_screening_time(self, obj):
        return obj.screening.time

    def get_seat(self, obj):
        return obj.seat


class ScreeningAdmin(admin.ModelAdmin):
    model = Screening
    list_display = (
        'movie',
        'theater',
        'auditorium',
        'time'
    )



admin.site.register(Movie, MovieAdmin)
admin.site.register(Theater, TheaterAdmin)
# admin.site.register(Stillcut)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Auditorium, AuditoriumAdmin)
# admin.site.register(Seat)
# admin.site.register(ReservedSeat)
admin.site.register(Screening, ScreeningAdmin)
# admin.site.register(ScreeningTime)
admin.site.register(Cast)
admin.site.register(Casting)
admin.site.register(Director)
admin.site.register(Directing)