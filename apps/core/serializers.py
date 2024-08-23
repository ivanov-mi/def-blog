from rest_framework import serializers
from .models import Post, Comment, Hashtag, Vote
from .utils import get_hashtags
from django.utils.timezone import now
from rest_framework.validators import UniqueTogetherValidator


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

    def validate(self, data):
        author = self.context.get('request').user
        post = data.get('post')

        if Vote.objects.filter(author=author, post=post).exists():
            raise serializers.ValidationError('You have already voted for this post. Users are allowed to vote only once for a single post.')

        return data
