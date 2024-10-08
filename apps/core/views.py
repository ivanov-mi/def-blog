from rest_framework.decorators import action
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Hashtag, Vote
from .serializers import PostSerializer, CommentSerializer, HashtagSerializer, VoteSerializer, PostDetailsSerializer
from .decorators import paginate
from .filters import PostFilter
from .permissions import IsOwnerOrAdminOrReadOnly, CommentsCustomPermission, VotesCustomPermissions, HashtagsCustomPermissions


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = PostFilter
    ordering_fields = ['date_posted']
    ordering = ['-date_posted']
    search_fields = ['title', 'hashtags__name']

    def retrieve(self, request, pk=None):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostDetailsSerializer(post)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @paginate(CommentSerializer)
    @action(detail=True, methods=['get'])
    def comments(self, request, *args, **kwargs):
        post = self.get_object()
        comments = post.comments.all()
        return comments


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [CommentsCustomPermission]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class HashtagViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    permission_classes = [HashtagsCustomPermissions]


class VoteViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [VotesCustomPermissions]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
