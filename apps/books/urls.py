from django.urls import path
from .views import BookListCreate, BookDetailView, BooksByAuthor

urlpatterns = [
    path("books/", BookListCreate.as_view()),
    path("book/<uuid:pk>/", BookDetailView.as_view()),
    path("book", BooksByAuthor.as_view())
]