from profiles.models import User, Projects
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","username_user",'email', "image_profile", "image_profile_project", "slug" ,"timestamp", "bio")
        read_only_fields = ('type','timestamp', 'slug')
        lookup_field = 'slug'

    def create(self, validated_data):
        return User.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.username_user = validated_data.get('username_user', instance.username_user)
        instance.email = validated_data.get('email', instance.email)
        instance.image_profile = validated_data.get('image_profile', instance.image_profile)
        instance.image_profile_project = validated_data.get('image_profile_project', instance.image_profile_project)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()
        return instance


class ProjectSerializer(serializers.ModelSerializer):
    # project = serializers.ChoiceField(choices=Projects.CHOICES_PROJECT)
    users = UserSerializer(read_only=True)
    image_project = serializers.ImageField(max_length=None, use_url=True, required=False)
    image_1= serializers.ImageField(max_length=None, use_url=True, required=False)
    image_2 = serializers.ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = Projects
        fields = ("id","title",'image_project', "image_1", "image_2","progress", "tentang", "pengertian", "kelebihan","tgl_project", "users" , "slug")
        read_only_fields = ('type','timestamp', 'slug')
        lookup_field = 'slug'

    def create(self, validated_data):
        return Projects.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance
