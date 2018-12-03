from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(User)

# User admin page에 Reservation 을 Inline으로 추가할 것.
# 빠른 예매 취소 등의 관리를 위한 페이지