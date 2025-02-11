from django.urls import path
from .views import AuthorListCreate, AuthorDetailView, AuthorsByAuthor

urlpatterns = [
    path("authors/", AuthorListCreate.as_view()),
    path("author/<uuid:pk>/", AuthorDetailView.as_view()),
    path("author", AuthorsByAuthor.as_view())
]