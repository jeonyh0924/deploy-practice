import datetime
import random
import string

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

    def distinct_update(modeladmin, request, queryset):
        distinct_movies = Movie.objects.order_by('title').distinct('title')
        Movie.objects.exclude(pk__in=distinct_movies.values_list('pk', flat=True)).delete()

    def reservation_score_update(modeladmin, request, queryset):
        for movie in queryset:
            movie.reservation_score = len(ReservedSeat.objects.filter(screening__movie=movie)) / len(
                    ReservedSeat.objects.all())
            movie.save()

    now_open_update.short_description = "현재 개봉작 업데이트"
    now_show_update.short_description = "현재 상영작 업데이트"
    distinct_update.short_description = "중복 영화 제거"
    reservation_score_update.short_description = "예매율 업데이트"

    list_display = ['title', 'pk', 'reservation_score']
    list_filter = (
        'genre',
        'now_open',
        'now_show',
    )
    inlines = [DirectingInline, CastingInline, StillcutInline]
    actions = [now_show_update, now_open_update, distinct_update, reservation_score_update]

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
    def default_seat_create(modeladmin, request, queryset):
        alphabet = string.ascii_uppercase
        for auditorium in queryset:
            for row in range(1, 11):
                for number in range(1, 11):
                    auditorium.seats.create(row=row, number=number, seat_name=f'{alphabet[row-1]}' + f'{number}')

    default_seat_create.short_description = "상영관 좌석 생성(10*10)"
    inlines = [ScreeningInline, SeatInline]
    list_display = ('name', 'theater', 'seats_no', 'get_movie')
    list_filter = (
        'theater__location',
        'theater__sub_location',
                   )
    actions = [default_seat_create]

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
    def make_random_reservations(modeladmin, request, queryset):
        for i in range(1, 31):
            screen = random.choice(Screening.objects.all())
            reservation = Reservation.objects.create(
                user=random.choice(User.objects.all()),
                screening=screen
            )
            ReservedSeat.objects.create(
                screening=screen,
                seat=random.choice(Seat.objects.filter(auditorium=screen.auditorium)),
                reservation=reservation
            )
    make_random_reservations.short_description = "무작위 예매 생성"
    model = Reservation
    list_display = ('user', 'pk', 'get_movie', 'get_theater', 'get_seat', 'is_active')
    actions = [make_random_reservations]

    def get_movie(self, obj):
        return obj.screening.movie

    def get_theater(self, obj):
        return obj.screening.theater

    def get_screening_time(self, obj):
        return obj.screening.time

    def get_seat(self, obj):
        return obj.seats_reserved.all()


class SeatAdmin(admin.ModelAdmin):
    model = Seat
    list_display = (
        'pk',
        'auditorium_name',
        'seat_name',
        'row',
        'number'
    )

    def auditorium_name(self, obj):
        return obj.auditorium.name

class ScreeningAdmin(admin.ModelAdmin):
    def make_random_screenings(modeladmin, request, queryset):
        start_pk = Theater.objects.first().pk
        last_pk = Theater.objects.last().pk
        for movie in Movie.objects.filter(now_show=False):
            pk = random.randrange(start_pk, last_pk + 1)
            try:
                theater = Theater.objects.get(pk=pk)
                auditorium = random.choice(theater.auditoriums.all())
                Screening.objects.create(
                    movie=movie,
                    theater=theater,
                    time=datetime.datetime.now(),
                    auditorium=auditorium)
            except ObjectDoesNotExist:
                pass

    make_random_screenings.short_description = "무작위 상영 인스턴스 생성"
    model = Screening
    list_display = (
        'movie',
        'pk',
        'theater',
        'auditorium',
        'time'
    )
    actions = [make_random_screenings]




admin.site.register(Movie, MovieAdmin)
admin.site.register(Theater, TheaterAdmin)
# admin.site.register(Stillcut)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Auditorium, AuditoriumAdmin)
admin.site.register(Seat, SeatAdmin)
admin.site.register(Screening, ScreeningAdmin)
admin.site.register(Cast)
# admin.site.register(Casting)
admin.site.register(Director)
# admin.site.register(Directing)
admin.site.register(ReservedSeat)
