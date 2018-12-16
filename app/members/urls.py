from django.urls import path
from . import apis

urlpatterns_api_members = ([
    path('login/', apis.AuthTokenView.as_view()),
    path('signup/', apis.SignupView.as_view()),
    path('profile/', apis.UserProfileView.as_view()),
    path('social-login/', apis.SocialAuthTokenView.as_view()),
    path('logout/', apis.LogoutView.as_view()),
    path('checkID/', apis.CheckUniqueIDView.as_view()),
    path('user-list/', apis.UserListView.as_view()),
    path('check-password/', apis.CheckPasswordView.as_view()),
    path('user-delete/', apis.UserDeleteView.as_view()),
    path('reservations/<int:pk>/', apis.UserReservationView.as_view()),
], 'members')