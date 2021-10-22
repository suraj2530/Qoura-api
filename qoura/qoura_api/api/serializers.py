from rest_framework import serializers
from django.contrib.auth.models import User
from qoura_api.models import (
    Question,
    Answer,
    Like
)
import re

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email"]

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email"]

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("This field may not be blank.")

        return value

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"
        read_only_fields = ['liker']

class AnswerSerializer(serializers.ModelSerializer):
    like = LikeSerializer(many=True, read_only=True)
    author_name = serializers.SerializerMethodField()
    
    def get_author_name(self, obj):
        return obj.author.username

    class Meta:
        model = Answer
        fields = "__all__"
        read_only_fields = ['author']

class QuestionSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer(many=True, read_only=True)
    author_name = serializers.SerializerMethodField()
    
    def get_author_name(self, obj):
        return obj.author.username

    # author = serializers.SerializerMethodField()
    # def get_author(self, obj):
    #     return obj.author.username

    class Meta:
        model = Question
        fields = "__all__"
        read_only_fields = ['url_title', 'author']

    def create_url(self):
        url_title = self.validated_data['title']
        url_title = re.sub(r'[^\w\s]', '', url_title)
        return url_title.strip().replace(" ", "-").lower()

