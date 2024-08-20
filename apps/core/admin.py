from django.contrib import admin
from .models import Post, Comment, Hashtag, Vote


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'date_posted')
    list_filter = ('author', 'date_posted')
    search_fields = ('title', 'content')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'post', 'author', 'date_created')
    list_filter = ('author', 'date_created')
    search_fields = ('title', 'content')


class HashtagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name', )


class VoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_liked', 'post', 'author', 'date_created')
    list_filter = ('is_liked', 'date_created')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Hashtag, HashtagAdmin)
admin.site.register(Vote, VoteAdmin)
