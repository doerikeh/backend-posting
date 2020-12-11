from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.decorators import api_view, parser_classes, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from kisahkita_art.models import Comment, Posting, Categories
from .serializers import CommentSerializer, PostingSerializer, CategoriesSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
import django_filters.filters
from rest_framework.response import Response

# from django.db.models import Q
from rest_framework.generics import ListAPIView
from django.db.models import Count, Q
class JsonResponse(HttpResponse):
    def __init__(self, data, **kwargs): 
        content = JSONRenderer().render(data)   
        kwargs['content_type'] = 'application/json'
        super(JsonResponse, self).__init__(content, **kwargs)

@api_view(['GET',"POST"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@csrf_exempt
def posting_list(request):
    if request.method == 'GET':
        posting = Posting.objects.all()
        posting_serializer = PostingSerializer(posting, many=True)
        return JsonResponse(posting_serializer.data)
    elif request.method == "POST":
        posting_data = JSONParser().parse(request.data)
        posting_serializer = PostingSerializer(data=posting_data)
        if posting_serializer.is_valid():
            posting_serializer.save()
            return JsonResponse(posting_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(posting_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE", "POST"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@csrf_exempt
def posting_detail(request, slug):
    try:
        posting = Posting.objects.get(slug=slug)
    except Posting.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        posting.viewed = posting.viewed + 1
        posting.save()
        posting_serializer = PostingSerializer(posting)
        return JsonResponse(posting_serializer.data)
    elif request.method == "POST":
        posting_serializer = PostingSerializer(posting, data=request.data)
        if posting_serializer.is_valid():
            posting_serializer.save()
            return JsonResponse(posting_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(posting_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "PUT":
        posting_serializer = PostingSerializer(posting, data=request.data)
        if posting_serializer.is_valid():
            posting_serializer.save()
            return JsonResponse(posting_serializer.data)
        return JsonResponse(posting_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        posting.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def categories_list(request):
    if request.method == "GET":
        categories = Categories.objects.all()
        categories_serializer = CategoriesSerializer(categories, many=True)
        return JsonResponse(categories_serializer.data)
    elif request.method == "POST":
        categories_data = JSONParser().parse(request.data)
        categories_serializer = CategoriesSerializer(data=categories_data)
        if categories_serializer.is_valid():
            categories_serializer.save()
            return JsonResponse(categories_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(categories_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def categories_detail(request, slug):
    try:
        categories = Categories.objects.get(slug=slug)
    except Categories.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        categories_serializer = CategoriesSerializer(categories)
        return JsonResponse(categories_serializer.data)
    elif request.method == "PUT":
        categories_serializer = CategoriesSerializer(categories, data=request.data)
        if categories_serializer.is_valid():
            categories_serializer.save()
            return JsonResponse(categories_serializer.data)
        return JsonResponse(categories_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        categories.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET',"POST"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@csrf_exempt
def posting_list_4(request):
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page = 4
        posting = Posting.objects.all()
        result_page = paginator.paginate_queryset(posting, request)
        posting_serializer = PostingSerializer(result_page, many=True)
        return paginator.get_paginated_response(posting_serializer.data)
    elif request.method == "POST":
        posting_data = JSONParser().parse(request.data)
        posting_serializer = PostingSerializer(data=posting_data, files=request.FILES)
        if posting_serializer.is_valid():
            posting_serializer.save()
            return JsonResponse(posting_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(posting_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FilterPosting(django_filters.FilterSet):
    class Meta:
        model = Posting
        fields = ["categories__title"]

class PostingFilterBody(ModelViewSet):
    queryset = Posting.objects.all()
    serializer_class = PostingSerializer
    lookup_field = "slug"
    filter_backends = (DjangoFilterBackend,)
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    filterset_class = FilterPosting

    def get_queryset(self):
        query = self.request.query_params.dict()
        keyword = query.get("q", None)
        query_data = self.queryset
        if keyword:
            query_data = query_data.filter(
                Q(title__icontains=keyword)|
                Q(title__iexact=keyword)|
                Q(categories__title__icontains=keyword)|
                Q(categories__title__iexact=keyword)
            ).distinct()
        return query_data
class CommentView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        query = self.request.query_params.dict()
        return self.queryset.filter(**query)


class TopPosting(ListAPIView):
    queryset = Posting.objects.all()
    serializer_class = PostingSerializer

    def get_queryset(self):
        posting = self.queryset.annotate(viewed_count=Count("viewed")).order_by("-viewed_count")[:5]
        return posting


class CommentPosting(ListAPIView):
    queryset = Posting.objects.all()
    serializer_class = PostingSerializer

    def get_queryset(self):
        posting_comment = self.queryset.annotate(comment_count=Count("post_comments")).order_by("-comment_count")[:6]
        return posting_comment


class CategoriesPosting(ListAPIView):
    serializer_class = CategoriesSerializer

    def get_queryset(self):
        queryset = Categories.objects.all()
        posting = self.request.query_params.get("posting_categories", None)
        if posting is not None:
            queryset = queryset.filter(posting_categories__title=posting)
        return queryset

    # def list(self, request, format=None):
    #     queryset = Categories.objects.filter(posting_categories__is_published=True)
    #     serializer = CategoriesSerializer(queryset, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    

# class SimiliarBlog(ListAPIView):
#     queryset = Posting.objects.all()
#     serializer_class = PostingSerializer

#     def get_queryset(self, request, *args, **kwargs):
#         posting_id = kwargs.get("posting_id")
#         try:
#             posting_categories = self.queryset.get(id=posting_id).categories.all()
#         except Exception:
#             return None
#         posting = self.queryset.filter(categories__id__in=[categories.id for categories in posting_categories]).exclude(id=posting_id)
#         return posting