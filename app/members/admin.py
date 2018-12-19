from django.contrib import admin
from .models import *
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    def make_default_user(modeladmin, request, query):
        for i in range(1, 51):
            User.objects.create(
                username=f"test{i}",
                password=1111,
                first_name=f"{i}",
                last_name=f"tester",
                email=f"tester{i}@test.com",
                phone_number="00000000000"
            )

    make_default_user.short_description = "기본 테스트 유저 생성"
    model = User
    actions = [make_default_user]
    list_display = (
        'username',
        'get_name',
    )

    def get_name(self, obj):
        return obj.last_name + obj.first_name

admin.site.register(User, UserAdmin)

# User admin page에 Reservation 을 Inline으로 추가할 것.
# 빠른 예매 취소 등의 관리를 위한 페이지