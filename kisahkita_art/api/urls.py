from django.urls import path, include
from .views import (posting_detail, posting_list, categories_detail, 
                    categories_list, posting_list_4, PostingFilterBody, CommentView,
                    TopPosting, CommentPosting, CategoriesPosting)
from rest_framework.routers import DefaultRouter

app_name = "kisahkita_art"

router = DefaultRouter()
router.register("filter", PostingFilterBody)
router.register("comment", CommentView)


urlpatterns =[
    path("posting/", posting_list, name="list"),
    path("postings/", posting_list, name="list-posting"),
    path("postings-list/", posting_list_4, name="list_page"),
    path("posting/<slug>/", posting_detail, name="detail"),
    path("postingss/", include(router.urls)),
    path("top-posting/", TopPosting.as_view()),
    path("comment-top/", CommentPosting.as_view()),
    path("categories-posting/", CategoriesPosting.as_view()),
    path("categories-posting/<slug>", CategoriesPosting.as_view()),
    # path("comment/", posting_comment, name="comment"),
    #path("similiar-posting/<int:posting_id>", SimiliarPostingView.as_view(), name="comment"),
    path("categories/", categories_list, name="categories-list"),
    path("categories/<slug>/", categories_detail, name="categories-detail")
]