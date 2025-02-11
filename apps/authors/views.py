from django.shortcuts import render
from datetime import timedelta
from django.utils import timezone
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, GenericAPIView
from rest_framework.exceptions import PermissionDenied
from .models import Author
from .serializers import AuthorSerializer
from apps.utils.response import CustomGenericAPIView

# Create your views here.

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

class AuthorsByAuthor(CustomGenericAPIView, ListAPIView):
    serializer_class = AuthorSerializer

    def get_queryset(self):
        username = self.request.query_params.get("username")
        if username:
            return Author.objects.filter(username__icontains=author_name)
        return Author.objects.none()