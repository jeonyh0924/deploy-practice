from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

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
class FacebookSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    last_name = serializers.CharField()
    first_name = serializers.CharField()
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
