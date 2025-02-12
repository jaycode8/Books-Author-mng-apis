from django.urls import path
from .views import AuthorListCreate, AuthorDetailView, AuthorAuthentication, AuthorProfileAPIView

urlpatterns = [
    path("authors/", AuthorListCreate.as_view()),
    path("author/<uuid:pk>/", AuthorDetailView.as_view()),
    path("login/", AuthorAuthentication.as_view()),
    path("profile/", AuthorProfileAPIView.as_view()),
]