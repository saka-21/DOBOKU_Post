from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, Post, Comment, Like
from django.contrib.auth.hashers import make_password  # 追加


class UserSerializer(serializers.ModelSerializer):
    """ユーザー一覧シリアライザー"""
    class Meta:
        model = get_user_model()
        fields = '__all__'
        # read_only_fields = ('last_login', 'is_superuser', 'is_staff', 'is_active', 'first_name', 'last_name', 'date_joined', 'groups', 'user_permissions')

    def create(self, validated_data):
        password = validated_data.get('password', None)
        if password is not None:
            validated_data['password'] = make_password(password)
        return super().create(validated_data)

    # def update(self, instance, validated_data):
    #     if 'password' in validated_data:
    #         instance.set_password(validated_data['password'])
    #     else:
    #         instance = super().update(instance, validated_data)
    #     instance.save()
    #     return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class PostSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all())
    author = UserSerializer(read_only=True)
    author_name = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(), write_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    image_change = serializers.ImageField(read_only=True)
    address = serializers.CharField(required=False)
    lat = serializers.DecimalField(
        required=False, max_digits=20, decimal_places=15,)
    lng = serializers.DecimalField(
        required=False, max_digits=20, decimal_places=15,)

    def get_likes_count(self, obj):
        return obj.like_post.count()

    def get_comments_count(self, obj):
        return obj.comment_post.count()

    def create(self, validated_data):
        validated_data['author'] = validated_data.get('author_name', None)

        if validated_data['author'] is None:
            raise serializers.ValidationError('author not found.')

        del validated_data['author_name']

        return Post.objects.create(**validated_data)

    class Meta:
        model = Post
        fields = ('id', 'category', 'author', 'author_name', 'title', 'content',
                  'published_at', 'image', 'likes_count', 'comments_count', 'image_change', 'prefecture', 'address', 'lat', 'lng')
        # fields = '__all__'
        # read_only_fields = ('like',)


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all())
    author = UserSerializer(read_only=True)
    author_name = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(), write_only=True)

    def create(self, validated_data):
        validated_data['author'] = validated_data.get('author_name', None)

        if validated_data['author'] is None:
            raise serializers.ValidationError('author not found.')

        del validated_data['author_name']

        return Comment.objects.create(**validated_data)

    class Meta:
        model = Comment
        # fields = '__all__'
        fields = ('id', 'post', 'author', 'author_name', 'text', 'timestamp')


class LikeSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    post_id = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(), write_only=True)

    def create(self, validated_date):
        validated_date['post'] = validated_date.get('post_id', None)
        if validated_date['post'] is None:
            raise serializers.ValidationError("post not found.")
        del validated_date['post_id']

        return Like.objects.create(**validated_date)

    class Meta:
        model = Like
        fields = ('id', 'user', 'post', 'post_id')