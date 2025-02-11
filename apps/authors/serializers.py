from rest_framework.serializers import ModelSerializer
from django.contrib.auth.hashers import make_password
from .models import Author

class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

    def create(self, validated_data):
        password = validated_data.pop("password")
        hashed_password = make_password(password)
        instance = super().create(validated_data)
        instance.password = hashed_password
        instance.save()
        return instance