from .tokens import create_jwt_pair_for_user
from . models import User
from user_profile.models import OwnerProfile
from . permission import IsOwnerOrReadObly
from rest_framework.decorators import api_view
from user_profile.models import TenetProfile, OwnerProfile
from django.shortcuts import render, redirect, HttpResponse
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, mixins
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login, logout
from .serializers import TenetRegistrationgSerializer, OwnerRegisterSerializer, TenetSerializer, OwnerSerializer, LoginSerializer

# Create your views here.


class TenetRegisterView(generics.GenericAPIView,
                        mixins.CreateModelMixin):
    serializer_class = TenetRegistrationgSerializer
    permission_classes = (AllowAny,)
    queryset = TenetProfile.objects.all()

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'message': "tenet created successfully",
            'data': serializer.data
        }
        return Response(data=response, status=status.HTTP_200_OK)


class TenetListView(generics.ListAPIView):
    serializer_class = TenetSerializer
    queryset = TenetProfile.objects.all()
    # permission_classes = [IsAdminUser]

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OwnerRegisterView(generics.CreateAPIView):
    serializer_class = OwnerRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "Owner Profile Created Successfully",
                "data": serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        response = {
            "message": serializer.errors
        }

        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class OwnerListView(generics.ListAPIView):
    serializer_class = OwnerSerializer
    queryset = OwnerProfile.objects.all()
    permission_classes = [IsAdminUser]

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes  = [AllowAny]
    def post(self, request: Request, format=None):
        data = request.data
        email = data.get('email', None)
        password = data.get('password', None)
        
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            
            tokens = create_jwt_pair_for_user(user)

            response = {
                'message':"Login Successfully",
                "Token":tokens
            }

            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request: Request):
        response = {
            "user": str(request.user),
            "auth": str(request.auth)
        }
        return Response(data=response, status=status.HTTP_200_OK)


class User_logout(APIView):
    permission_classes = [IsAuthenticated]
    

    def get(self, request: Request, *args, **kwargs):
        
      
        request.user.auth_token.delete()
        logout(request)
        response = {
            "message": "Logout Successfully"
        }
        return Response(data=response, status=status.HTTP_200_OK)
    
    


