from qoura_api.api.serializers import (
    UserListSerializer,
    UserCreateSerializer,
    QuestionSerializer,
    AnswerSerializer,
    LikeSerializer
)
from qoura_api.api.permissions import (
    IsAuthor
)
from qoura_api.models import (
    Question,
    Answer,
    Like
)
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets
from rest_framework.authentication import (TokenAuthentication, SessionAuthentication)
from rest_framework.decorators import authentication_classes  
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser]

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

@authentication_classes((TokenAuthentication, SessionAuthentication))
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    #permission_classes = [IsAdminUser]

    def retrieve(self, request, pk=None):
        if request.user and pk == 'me':
            return Response(UserListSerializer(request.user).data)

        if request.user.is_superuser:
            return super(UserDetail, self).retrieve(self, request, pk=None)

        return Response(
                "Authentication credentials were not provided.",
                status=status.HTTP_403_FORBIDDEN, content_type=403)

    def get_queryset(self):
        if 'auth_token' in self.kwargs.keys():
            auth_token = self.kwargs['auth_token']
            self.lookup_field = 'auth_token'
            return User.objects.filter(auth_token=auth_token)
        
        return self.queryset

class QuestionDetail(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    
    def get_queryset(self):
        if 'url_title' in self.kwargs.keys():
            url_title = self.kwargs['url_title']
            self.lookup_field = 'url_title'
            return Question.objects.filter(url_title=url_title)
        
        return self.queryset
    

@authentication_classes((TokenAuthentication, SessionAuthentication))
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('-id')
    #id_author = Question.objects.values('author')
    serializer_class = QuestionSerializer

    # def get_serializer_class(self):
    #     if self.action == 'create' or self.action == 'update':
    #         return QuestionCreateSerializer

    #     return QuestionSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if self.request.user.id != instance.author.id:
            return Response(
                "Only the author can delete the question.",
                status=status.HTTP_401_UNAUTHORIZED, content_type=401)

        self.perform_destroy(instance)
        return Response("Deleted successfully.", status=status.HTTP_204_NO_CONTENT)

    def perform_update(self, serializer):
        serializer.save(url_title=serializer.create_url())

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, url_title=serializer.create_url())

@authentication_classes((TokenAuthentication, SessionAuthentication))
class AnswerList(generics.ListAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def get_queryset(self):
        if 'url_title' in self.kwargs.keys():
            url_title = self.kwargs['url_title']
            self.lookup_field = 'url_title'
            return Answer.objects.filter(question__url_title=url_title).order_by('-id')       
        return self.queryset

@authentication_classes((TokenAuthentication, SessionAuthentication))
class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@authentication_classes((TokenAuthentication, SessionAuthentication))
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        serializer.save(liker=self.request.user)
