from django.contrib import admin
import nested_admin
from nested_admin.nested import NestedModelAdmin
from reservations.models import *

# 극장의 many_to_many 필드 구현
# 각 change list 페이지에 filter & search 기능 달기
# now_show 항목 업데이트 버튼 만들기
# 좌석 bulk create 기능 가능 여부
# image 프리뷰 달기
# custom button & custom View 생성 여부 > 영화 검색기능 달기(영화진흥위원회 Open API 활용)
# 관리자 기능 마무리되면 admin page 템플릿 조정


# 영화 Admin setting
class StillcutInline(admin.StackedInline):
    model = Stillcut
    extra = 1


class MovieAdmin(admin.ModelAdmin):
    list_display = ['title']
    inlines = [StillcutInline]

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
    inlines = [ScreeningInline, SeatInline]
    list_display = ('name', 'theater', 'seats_no')


class AuditoriumInline(nested_admin.nested.NestedStackedInline):
    model = Auditorium
    extra = 1


# 극장 admin setting
class TheaterAdmin(nested_admin.nested.NestedModelAdmin):
    model = Theater
    inlines = [AuditoriumInline]
    list_display = ('sub_location', 'location', 'get_auditorium')

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