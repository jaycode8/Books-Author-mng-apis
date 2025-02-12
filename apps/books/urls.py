from django.urls import path
from .views import BookListView, BookDetailView, BooksByAuthor, CreateBookPIView

urlpatterns = [
    path("books/", BookListView.as_view()),
    path("book", CreateBookPIView.as_view()),
    path("book/<uuid:pk>/", BookDetailView.as_view()),
    path("books/author", BooksByAuthor.as_view()),
]