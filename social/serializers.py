from rest_framework import serializers

from social.models import Profile, Post
from user.serializers import UserSerializer


class ProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            "id",
            "full_name",
            "avatar",
            "gender",
            "followers_count",
            "posts_count",
        )

    def get_followers_count(self, obj):
        return obj.following.count()

    def get_posts_count(self, obj):
        return obj.posts.count()


class ProfilePostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "title", "created_at",)


class ProfileDetailSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    user = UserSerializer(many=False, read_only=True)
    posts = ProfilePostsSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "posts",
            "first_name",
            "last_name",
            "avatar",
            "biography",
            "gender",
            "following",
            "followers",
        )

    def get_followers(self, obj):
        return list(obj.followers.all().values_list('full_name', flat=True))

    def get_following(self, obj):
        return list(obj.following.all().values_list('profiles__full_name', flat=True))


class ProfileCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "first_name",
            "last_name",
            "avatar",
            "gender",
            "following",
        )


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="profile.full_name")

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "title",
            "content",
            "media_attachments",
            "hashtag",
            "created_at",
        )
        read_only_fields = [
            "author",
        ]


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "profile",
            "title",
            "content",
            "media_attachments",
            "hashtag",
            "created_at",
        )
        read_only_fields = [
            "author",
            "profile",
        ]
