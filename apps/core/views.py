from rest_framework.decorators import action
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Hashtag, Vote
from .serializers import PostSerializer, CommentSerializer, HashtagSerializer, VoteSerializer, PostDetailsSerializer
from rest_framework.pagination import PageNumberPagination
from .decorators import paginate


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination

    def retrieve(self, request, pk=None):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostDetailsSerializer(post)
        return Response(serializer.data)

    @paginate(CommentSerializer)
    @action(detail=True, methods=['get'])
    def comments(self, request, *args, **kwargs):
        post = self.get_object()
        comments = post.comments.all()
        return comments


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class HashtagViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer


class VoteViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
