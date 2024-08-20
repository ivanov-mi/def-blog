from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import PostViewSet, HashtagViewSet, CommentViewSet, VoteViewSet


router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'hashtags', HashtagViewSet, basename='hashtag')
router.register(r'votes', VoteViewSet, basename='vote')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),
    path('', include(router.urls))
]
