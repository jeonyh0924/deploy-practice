from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
# from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    class Meta:
        verbose_name = '유저'
        verbose_name_plural = f'{verbose_name} 목록'

    phone_number = models.CharField('Phone Number', max_length=20, blank=True)

    # facebook, google의 경우 first name과 last name으로 분리하기 용이
    # kakao의 경우 받은 데이터를 세이브하는 과정에서 비어있는 영역을 채울 수 있는
    # 별도의 form을 생성해 KakaoSignupForm(request.POST).save()를 구현하자.

    # 혹은 UserManager에서 create_user와 같은 method를 새롭게 지정하여
    # 이를 CustomUserModel에서 name = first_name + last_name으로 받을 수 있다.
