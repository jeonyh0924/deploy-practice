from django.contrib import admin
from .models import *
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = (
        'username',
        'get_name',
    )

    def get_name(self, obj):
        return obj.last_name + obj.first_name

admin.site.register(User, UserAdmin)

# User admin page에 Reservation 을 Inline으로 추가할 것.
# 빠른 예매 취소 등의 관리를 위한 페이지