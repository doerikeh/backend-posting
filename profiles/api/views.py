from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.decorators import api_view, parser_classes, authentication_classes, permission_classes
from rest_framework import status
from profiles.models import Projects, User
from .serializers import UserSerializer, ProjectSerializer

class JsonResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)   
        kwargs['content_type'] = 'application/json'
        super(JsonResponse, self).__init__(content, **kwargs)

@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def profiles_detail(request, slug):
    try:
        user = User.objects.get(slug=slug)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        user_serializer = UserSerializer(user)
        return JsonResponse(user_serializer.data)
    elif request.method == "PUT":
        user_serializer = UserSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data)
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        user.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET',"POST"])
@parser_classes([FormParser, MultiPartParser])
@csrf_exempt
def profiles(request):
    if request.method == 'GET':
        user = User.objects.all()
        user_serializer = UserSerializer(user, many=True)
        return JsonResponse(user_serializer.data)
    elif request.method =="POST":
        project_data = JSONParser().parse(request.data)
        user_serializer = UserSerializer(data=project_data, files=request.FILES)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET',"POST"])
@parser_classes([FormParser, MultiPartParser])
@csrf_exempt
def project_list(request):
    if request.method == 'GET':
        projects = Projects.objects.all()
        projects_serializer = ProjectSerializer(projects, many=True)
        return JsonResponse(projects_serializer.data)
    elif request.method =="POST":
        project_data = JSONParser().parse(request.data)
        projects_serializer = ProjectSerializer(data=project_data, files=request.FILES)
        if projects_serializer.is_valid():
            projects_serializer.save()
            return JsonResponse(projects_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(projects_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', "PUT", "DELETE"])
@csrf_exempt
def project_detail(request, slug):
    try:
        project = Projects.objects.get(slug=slug)
    except Projects.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        projects_serializer = ProjectSerializer(project)
        return JsonResponse(projects_serializer.data)
    elif request.method == "PUT":
        projects_serializer = ProjectSerializer(project, data=request.data)
        if projects_serializer.is_valid():
            projects_serializer.save()
            return JsonResponse(projects_serializer.data)
        return JsonResponse(projects_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        project.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
