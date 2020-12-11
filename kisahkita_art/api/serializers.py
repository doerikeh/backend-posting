from kisahkita_art.models import Categories, Posting, Comment
from profiles.api.serializers import UserSerializer
from rest_framework import serializers

class PostingSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField("get_image")
    user      = UserSerializer(read_only=True)
    viewed_count = serializers.SerializerMethodField("get_viewed_count")
    comment_count = serializers.SerializerMethodField("get_comment_count")
    class Meta:
        model = Posting
        fields = ("id","title", "categories","viewed","date_created", "images", "image_url","slug", "posting", "is_published","user", "post_comments", "viewed_count", "comment_count")
        read_only_fields = ("type", "date_created", "slug", "post_comments",)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

    def get_image(self, obj):
        return obj.images.url
    
    def get_viewed_count(self, obj):
        return obj.viewed

    def get_comment_count(self, obj):
        return obj.post_comments.count()


class CategoriesSerializer(serializers.ModelSerializer):
    posting_categories = PostingSerializer(many=True, read_only=True)
    class Meta:
        model = Categories
        fields = ("id", "title", "slug", "image", "date_created", "posting_categories")
        read_only_fields = ("type", "date_created", "slug")
        lookup_field = 'slug'
class CommentSerializer(serializers.ModelSerializer):
    posting = PostingSerializer(read_only=True)
    posting_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("type", "date_created",)