import jwt
import datetime
from datetime import timedelta
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, GenericAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.exceptions import PermissionDenied
from .models import Author
from .serializers import AuthorSerializer
from apps.utils.response import CustomGenericAPIView
from apps.utils.token import JWTAuthentication

# Create your views here.
class AuthorProfileAPIView(RetrieveAPIView, CustomGenericAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Return the authenticated user's profile"""
        print(self.request.user.id)
        return self.request.user


class AuthorAuthentication(CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def create(self, request):
        data = JSONParser().parse(request)
        username = data['username']
        password = data['password']
        author = Author.objects.filter(username=username).first()

        try:
            user = get_object_or_404(Author, username=username)
        except:
            return Response({
                "status": 404,
                "message": "Username doest not exist"
            }, status=404)
            
        if not user.check_password(password):
            return Response({
                "status": 403,
                "message": "Incorect password"
            }, status=403)

        token = jwt.encode(
            {"id": str(author.id), "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)},
            settings.SECRET_KEY,
            algorithm="HS256"
        )
        return Response({
            "status": 200,
            "message": "Login successful",
            "token": token,
        }, status=200)

class AuthorListCreate(CustomGenericAPIView, ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class AuthorDetailView(RetrieveUpdateDestroyAPIView, CustomGenericAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def perform_destroy(self, instance):
        if timezone.now() - instance.created_at < timedelta(days=1):
            raise PermissionDenied("Unauthorized to delete an Author less 24hrs since creation")
        instance.delete()