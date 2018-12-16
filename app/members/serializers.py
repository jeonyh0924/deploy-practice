from datetime import datetime

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from mappings.models import Reservation
from mappings.serializers import SeatSerializer, ReservedSeatSerializer

User = get_user_model()

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'password',
            'last_name',
            'first_name',
            'email',
            'phone_number',
        )


# Sign Up > Username 중복 검사 Serializer
class CheckUniqueIDSerializer(serializers.Serializer):
    username = serializers.CharField()


# Facebook User Serializer
class SocialAccountSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    last_name = serializers.CharField(allow_blank=True, allow_null=True)
    first_name = serializers.CharField(allow_blank=True, allow_null=True)
    email = serializers.CharField(allow_blank=True, allow_null=True)
    phone_number = serializers.CharField(allow_blank=True, allow_null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, data):
        username = data['user_id']
        user = authenticate(username=username)
        if not user:
            user = User.objects.create_user(
                username=username,
                last_name=data['last_name'],
                first_name=data['first_name'],
                email=data['email'],
                phone_number=data['phone_number'],
            )
        self.user = user
        return data


# Check User Reservation Serializer
class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    screening_set = serializers.SerializerMethodField()
    seats_reserved = ReservedSeatSerializer(many=True)
    num = serializers.SerializerMethodField()

    # 여기서 return된 pk는 "예매번호" 로 사용할 수 있도록 한다.
    class Meta:
        model = Reservation
        fields = (
            'pk',
            'user',
            'screening_set',
            'num',
            'seats_reserved',
            'is_active',
        )
        read_only_fields = (
            'user',
        )

    def get_screening_set(self, reservation):
        request = self.context.get("request")
        screen = reservation.screening
        movie = screen.movie
        try:
            img_url = request.build_absolute_uri(movie.main_img.url)
            thumb_img_url = request.build_absolute_uri(movie.thumbnail_img.url)
        except AttributeError:
            img_url = ""
            thumb_img_url = ""
        title = movie.title
        age = movie.age
        theater = screen.theater.sub_location
        time = datetime.strftime(screen.time, "%Y-%m-%d %H:%M")
        return {
            "img_url": img_url,
            "thumb_img_url": thumb_img_url,
            "title": title,
            "age": age,
            "theater": theater,
            "time": time
        }

    def get_num(self, reservation):
        return len(reservation.seats_reserved.all())