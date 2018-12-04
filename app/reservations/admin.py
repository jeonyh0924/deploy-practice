import datetime

from django.contrib import admin
import nested_admin
from django.shortcuts import render
from django.utils import timezone
from nested_admin.nested import NestedModelAdmin
from reservations.models import *


# 좌석 bulk create 기능 가능 여부
# image 프리뷰 달기
# custom button & custom View 생성 여부 > 영화 검색기능 달기(영화진흥위원회 Open API 활용)
# 관리자 기능 마무리되면 admin page 템플릿 조정


# 영화 Admin setting
class StillcutInline(nested_admin.nested.NestedStackedInline):
    model = Stillcut
    extra = 1


class CastInline(nested_admin.nested.NestedStackedInline):
    model = Cast
    extra = 1


class MovieAdmin(nested_admin.nested.NestedModelAdmin):
    def now_show_update(modeladmin, request, queryset):
        for movie in queryset:
            if movie.opening_date <= datetime.date.today():
                movie.now_show = True
                movie.save()

    now_show_update.short_description = "현재 상영작 업데이트"

    list_display = ['title']
    list_filter = (
        'genre',
        'now_show',
    )
    inlines = [CastInline, StillcutInline]
    actions = [now_show_update]

    def save_model(self, request, obj, form, change):
        super(MovieAdmin, self).save_model(request, obj, form, change)
        for file in request.FILES.getlist('photos_multiple'):
            obj.images.create(file=file)



# 상영 Admin setting
class ScreeningTimeInline(nested_admin.nested.NestedTabularInline):
    model = ScreeningTime
    extra = 1


class ScreeningAdmin(nested_admin.nested.NestedModelAdmin):
    inlines = [ScreeningTimeInline]


# 상영관 Admin setting
class ScreeningInline(nested_admin.nested.NestedStackedInline):
    model = Screening
    extra = 1
    inlines = [ScreeningTimeInline]

class SeatInline(nested_admin.nested.NestedTabularInline):
    model = Seat
    extra = 1


# 상영관 Admin setting
class AuditoriumAdmin(nested_admin.nested.NestedModelAdmin):
    # def seat_update(modeladmin, request, queryset):
    #     for auditorium in queryset:
    #         return render(request, 'admin/seateditor.html', context={})
    inlines = [ScreeningInline, SeatInline]
    list_display = ('name', 'theater', 'seats_no')
    list_filter = (
        'theater__location',
        'theater__sub_location',
                   )
    # actions = [seat_update]


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
        auditoriums = obj.auditorium_set.all()
        return [auditorium for auditorium in auditoriums]


class ReservationAdmin(admin.ModelAdmin):
    model = Reservation
    list_display = ('user', 'get_movie', 'get_theater', 'screening_time', 'get_seat', 'is_active')

    def get_movie(self, obj):
        return obj.screening.movie

    def get_theater(self, obj):
        return obj.screening.theater

    def get_seat(self, obj):
        return obj.selected_seats


admin.site.register(Movie, MovieAdmin)
admin.site.register(Theater, TheaterAdmin)
# admin.site.register(Stillcut)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Auditorium, AuditoriumAdmin)
# admin.site.register(Seat)
# admin.site.register(SelectedSeat)
# admin.site.register(Screening, ScreeningAdmin)
# admin.site.register(ScreeningTime)