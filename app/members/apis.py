from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions, generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import RetrieveUpdateAPIView

from .serializers import UserSerializer, FacebookSerializer, CheckUniqueIDSerializer
# from rest_framework.authtoken.serializers import AuthCustomTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
User = get_user_model()


# Local Signup APIView
class SignupView(generics.CreateAPIView):
    """
    username / password / last_name / first_name / email / phone_number드
    6개 필드 (pk 제외, 자동으로 생성)에 대한 값을 입력하여 POST요청
    필드값을 적절히 DB에 저장해 User Object 생성
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # method for creating password hashing relation
    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


# Check Username exists APIView
class CheckUniqueIDView(APIView):
    def post(self, request):
        # response = {}
        serializer = CheckUniqueIDSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(username=serializer.data['username'])
            if not user.exists():
                return Response({"username": serializer.data['username'], "message": '사용 가능한 아이디입니다.'}, status=status.HTTP_200_OK)
            return Response({"message": '이미 존재하는 아이디입니다.'}, status=status.HTTP_200_OK)


# Local Login APIView
class AuthTokenView(APIView):
    """
    POST요청으로 username, password를 받아
    사용자 인증(authenticate)에 성공하면(DB에 해당 User가 있는지 확인)
    해당 사용자와 연결된 토큰 정보 리턴
    """
    throttle_classes = ()
    permission_classes = ()

    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Social Account Signup-Login APIView
class FacebookAuthTokenView(APIView):
    """
    facebook SDK를 통해 얻은 사용자 정보를
    다음과 같은 5개 필드에 담아 JSON형식 - POST 요청으로 전송
    user_id / last_name / first_name / email / phone_number
    여기서 email, phone_number는 빈 데이터가 와도 받을 수 있다.
    받은 데이터의 user_id를 authenticate로 확인하여 이미 유저가 존재할 경우
    해당 유저에 Auth Token을 부여한다.
    만약 DB에 존재하지 않는 유저 정보일 경우, 해당 정보로 새로운 유저를 생성
    해당 유저에 Auth Token을 부여한다.

    """
    def post(self, request):
        serializer = FacebookSerializer(data=request.data)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Profile APIView
# Profile이므로 Username은 변경 불가로,
# Password는 ********로 표시하도록 한다.
class UserProfileView(RetrieveUpdateAPIView):
    """
    get요청 시 현재 Authenticated 유저의 유저정보가 담긴 Profile 데이터 리턴
    patch요청 시 수정한 데이터를 Authenticated 유저의 정보에 Save
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    # members/profile/로 받기 때문에, pk가 추가 인자로 들어오지 않는다.
    # 따라서 lookup_urlkwarg / lookup_field > 기본값 "pk"가 주어지지 않은 경우
    # request.user를 선택하여 리턴하도록 한다.
    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        if lookup_url_kwarg not in self.kwargs:
            return self.request.user


# Logout View
class LogoutView(APIView):
    """
    GET 요청으로 로그아웃 요청을 받는다
    해당 유저(request.user)가 가진 auth_token(Token object의 related_name)을 삭제
    """
    def get(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)