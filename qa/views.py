from django.shortcuts import render
from django.http import HttpResponseRedirect
from rest_framework.decorators import action
from .models import *

from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *

from knox.models import AuthToken
from django.conf import settings
import json

#https://medium.com/a-layman/build-single-page-application-with-react-and-django-part-1-connect-react-app-with-django-app-dbf6b5ec52f4

# Page API
class PageViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        orphan = self.request.query_params.get('orphan')

        if user_id and orphan:
            queryset = Page.objects.filter(creator=user_id, parent=None)
        elif user_id:
            queryset = Page.objects.filter(creator=user_id)
        elif orphan:
            queryset = Page.objects.filter(parent=None)
        else:
            queryset = Page.objects.all()

        # get the pages first 
        if queryset.order_by('id').count() == 0:
            #PATCH:if the user has no page, then create a default one
            data = {
                'name': 'Untitled',
                'parent': None, 
                'creator': user_id,
                'children': [], 
                'page_elements':[], 
                'group':1
            }
            json_string = json.dumps(data)
            serializer = AddPageSerializer(data=json.loads(json_string))
            if serializer.is_valid():
                serializer.save()
            else: 
                print(serializer.errors)

        return queryset.order_by('id')

    serializer_class = PageSerializer

# Add Page API
class AddPageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = AddPageSerializer

# Page_element API
class Page_elementViewSet(viewsets.ModelViewSet):
    queryset = Page_element.objects.select_related('question').all().order_by('order_on_page') # Page_element.objects.all().order_by('order_on_page')
    serializer_class = Page_elementSerializer

# Heading_1 API
class Heading_1ViewSet(viewsets.ModelViewSet):
    queryset = Heading_1.objects.all()
    serializer_class = Heading_1Serializer

# Heading_2 API
class Heading_2ViewSet(viewsets.ModelViewSet):
    queryset = Heading_2.objects.all()
    serializer_class = Heading_2Serializer

# Text API
class TextViewSet(viewsets.ModelViewSet):
    queryset = Text.objects.all()
    serializer_class = TextSerializer

# Question API
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    # API: remove question's tag
    @action(detail=True, methods=['post'])
    def remove_tag(self, request, pk=None):
        question = self.get_object()
        # Assuming you send the tag_name in the request data
        tag_name = request.data.get('tag_name')
        if not tag_name:
            return Response({'error': 'Tag name is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Use the remove() method to remove the specified tag
            question.tags.remove(tag_name)
            question.save()
            # Serialize the updated Question object and return it in the response
            serializer = self.get_serializer(question)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # API: add question's tag
    @action(detail=True, methods=['post'])
    def add_tag(self, request, pk=None):
        question = self.get_object()
        # Assuming you send the tag_name in the request data
        tag_name = request.data.get('tag_name')
        if not tag_name:
            return Response({'error': 'Tag name is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Use the add() method to add the specified tag
            question.tags.add(tag_name)
            question.save()
            # Serialize the updated Question object and return it in the response
            serializer = self.get_serializer(question)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Answer API
class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    # API: add favorite for an answer
    @action(detail=True, methods=['patch'])
    def add_favorite(self, request, pk=None):
        try:
            answer = self.get_object()
            user_id = request.data.get('user_id')

            if user_id:
                user = User.objects.get(pk=user_id)
                if user not in answer.a_vote_ups.all():
                    answer.a_vote_ups.add(user)
                    answer.save()
                    # Serialize the updated answer object and return it in the response
                serializer = self.get_serializer(answer)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'user_id not provided'}, status=400)
        except Answer.DoesNotExist:
            return Response({'error': 'Answer not found'}, status=404)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=400)

    # API: remove favorite for an answer
    @action(detail=True, methods=['patch'])
    def remove_favorite(self, request, pk=None):
        try:
            answer = self.get_object()
            user_id = request.data.get('user_id')

            if user_id:
                user = User.objects.get(pk=user_id)
                if user in answer.a_vote_ups.all():
                    answer.a_vote_ups.remove(user)
                    answer.save()
                    # Serialize the updated answer object and return it in the response
                serializer = self.get_serializer(answer)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'user_id not provided'}, status=400)
        except Answer.DoesNotExist:
            return Response({'error': 'Answer not found'}, status=404)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=400)

# Notification API
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        # Retrieve the current user from the request
        user = self.request.user
        # Perform the filtering based on the user
        queryset = Notification.objects.filter(noti_receiver=user).order_by('-date_created')
        return queryset

# Kanban API
class KanbanViewSet(viewsets.ModelViewSet):
    queryset = Kanban.objects.all()
    serializer_class = KanbanSerializer

# Kanban_Group API
class Kanban_GroupViewSet(viewsets.ModelViewSet):
    queryset = Kanban_Group.objects.all()
    serializer_class = Kanban_GroupSerializer

    def get_queryset(self):
        return Kanban_Group.objects.all()

# Kanban_Card API
class Kanban_CardViewSet(viewsets.ModelViewSet):
    queryset = Kanban_Card.objects.all().order_by('order_on_group')
    serializer_class = Kanban_CardSerializer

# PageLink API
class PageLinkViewSet(viewsets.ModelViewSet):
    queryset = PageLink.objects.all()
    serializer_class = PageLinkSerializer

# PageLink API
class ToDoViewSet(viewsets.ModelViewSet):
    queryset = To_do.objects.all()
    serializer_class = ToDoSerializer

# Table API
class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

# Table Row API
class TableRowViewSet(viewsets.ModelViewSet):
    queryset = Table_row.objects.all()
    serializer_class = TableRowSerializer

# Table Data API
class TableDataViewSet(viewsets.ModelViewSet):
    queryset = Table_data.objects.all()
    serializer_class = TableDataSerializer

# Tag API
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

# Register API 
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

#Login API
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

#Get User API
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user