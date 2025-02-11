from django.shortcuts import render
from datetime import timedelta
from django.utils import timezone
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, GenericAPIView
from rest_framework.exceptions import PermissionDenied
from .models import Book
from .serializers import BookSerializer
from .response import CustomGenericAPIView

# Create your views here.

class BookListCreate(CustomGenericAPIView, ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetailView(RetrieveUpdateDestroyAPIView, CustomGenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_destroy(self, instance):
        if timezone.now() - instance.created_at < timedelta(days=1):
            raise PermissionDenied("Unauthorized to delete a book less 24hrs since creation")
        instance.delete()

class BooksByAuthor(CustomGenericAPIView, ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        author_name = self.request.query_params.get("author")
        if author_name:
            return Book.objects.filter(author__icontains=author_name)
        return Book.objects.none()