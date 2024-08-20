from django.db import models
from .utils import get_hashtags
from authentication.models import CustomUser


class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f'#{self.name}'


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    hashtags = models.ManyToManyField(Hashtag, blank=True, related_name='posts')

    class Meta:
        ordering = ['date_posted']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

        new_hashtag_names = set(get_hashtags(self.content))
        if not new_hashtag_names:
            return

        existing_hashtags = Hashtag.objects.filter(name__in=new_hashtag_names)
        existing_hashtag_names = set(existing_hashtags.values_list('name', flat=True))

        # Create new unique hashtag objects
        unique_hashtag_names = new_hashtag_names.difference(existing_hashtag_names)
        new_hashtags = [Hashtag(name=hashtag_name) for hashtag_name in unique_hashtag_names]
        Hashtag.objects.bulk_create(new_hashtags)

        # Add hashtag references to current post
        self.hashtags.set(list(existing_hashtags) + new_hashtags)


    @property
    def likes(self):
        return self.votes.filter(is_liked=True).count()

    @property
    def dislikes(self):
        return self.votes.filter(is_liked=False).count()

    @property
    def rating(self):
        return self.likes - self.dislikes

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="author")

    class Meta:
        ordering = ['date_created']

    def __str__(self):
        return self.content


class Vote(models.Model):
    is_liked = models.BooleanField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="votes")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'author')
