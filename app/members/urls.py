from django.urls import path
from . import apis

urlpatterns_api_members = ([
  path('login/', apis.AuthTokenView.as_view()),
  path('signup/', apis.SignupView.as_view()),
  path('profile/', apis.UserProfileView.as_view()),
  path('facebook-login/', apis.FacebookAuthTokenView.as_view()),
  path('logout/', apis.LogoutView.as_view()),
  path('checkID/', apis.CheckUniqueIDView.as_view()),
], 'members')