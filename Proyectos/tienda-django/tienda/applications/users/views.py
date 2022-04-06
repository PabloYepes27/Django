from rest_framework.views import APIView

from django.shortcuts import render

from django.views.generic import TemplateView

from .serializers import LoginSocialSerializer


class LoginUser(TemplateView):
    template_name = 'users/login.html'


class GoogleLoginView(APIView):

    serializer_class = LoginSocialSerializer

