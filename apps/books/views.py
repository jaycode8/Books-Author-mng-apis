from django.shortcuts import render
from rest_framework.parsers import JSONParser
from datetime import timedelta
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, GenericAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.exceptions import PermissionDenied
from .models import Book
from .serializers import BookSerializer
from .response import CustomGenericAPIView
from apps.utils.token import JWTAuthentication
from apps.authors.models import Author
from apps.authors.serializers import AuthorSerializer

# Create your views here.
class CreateBookPIView(CreateAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        try:
            book = Book(title=data["title"], description=data["description"], price=data["price"], author=request.user)
            book.save()
            return Response({
                "status": 200,
                "message": "Successfully added a new book"
            }, status=200)
        except:
            return Response({
                "status": 403,
                "message": "An error has occured please try again later"
            }, status=403)

class BookListView(CustomGenericAPIView, ListAPIView):
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
            return Book.objects.filter(author__username__icontains=author_name)
        return Book.objects.none()