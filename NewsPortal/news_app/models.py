from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Puser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        rating = self.comment_set.exclude(post__author__puser=self).aggregate(Sum('rating'))['rating__sum']
        if author := getattr(self, 'author', False):
            rating += 3 * author.post_set.aggregate(Sum('rating'))['rating__sum']
            rating += author.post_set.aggregate(Sum('comment__rating'))['comment__rating__sum']
        self.rating = rating


class Author(models.Model):
    puser = models.OneToOneField(Puser, on_delete=models.CASCADE, primary_key=True)


class Category(models.Model):
    category = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    article = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1

    def preview(self):
        return self.text[:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    puser = models.ForeignKey(Puser, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1
