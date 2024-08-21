from rest_framework import serializers
from .models import Post, Comment, Hashtag, Vote
from .utils import get_hashtags
from django.utils.timezone import now


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['id', 'name']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    post_id = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), source='post')

    class Meta:
        model = Comment
        fields = ['id', 'content', 'post_id', 'author', 'date_created']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    rating = serializers.ReadOnlyField()
    hashtags = HashtagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'date_posted', 'rating', 'author', 'hashtags']

    def validate_hashtags(self, text):
        content = text.get('content')
        hashtags = get_hashtags(content)
        if len(hashtags) > 10:
            raise serializers.ValidationError('Maximum allowed number of hashtags is 10.')
        return text


class PostDetailsCommentSerializer(CommentSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'date_created']


class PostDetailsSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    rating = serializers.ReadOnlyField()
    hashtags = HashtagSerializer(many=True, read_only=True)
    comments = PostDetailsCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'date_posted', 'rating', 'author', 'comments', 'hashtags']


class VoteSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    post_id = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), source='post')

    class Meta:
        model = Vote
        fields = ['id', 'author', 'post_id', 'is_liked', 'date_created']

    def create(self, validated_data):
        vote, created = Vote.objects.get_or_create(
            author=validated_data['author'],
            post=validated_data['post']
        )

        vote.date_created = now()
        vote.is_liked = validated_data['is_liked']

        return vote
