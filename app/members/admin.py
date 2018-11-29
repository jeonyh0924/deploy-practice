from django.contrib import admin
from reservations.models import *

admin.site.register(Movie)
admin.site.register(Theater)
admin.site.register(Reservation)
admin.site.register(Auditorium)
admin.site.register(Seat)
admin.site.register(Screening)
# 극장 상영관 좌석 스크린