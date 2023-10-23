from django.db import models
from django.db.models import Sum
# from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

class Author(models.Model):
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        self.rating = 0
        if Post.objects.filter(author__user=self.user, type=Post.ARTICLE).exists():
            article_user = Post.objects.filter(author__user=self.user, type=Post.ARTICLE)
            self.rating += article_user.aggregate(Sum('rating'))['rating__sum'] * 3
            for article in article_user:
                self.rating += Comment.objects.filter(post=article).aggregate(Sum('rating'))['rating__sum']
        if Comment.objects.filter(user=self.user).exists():
            self.rating += Comment.objects.filter(user=self.user).aggregate(Sum('rating'))['rating__sum']
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=16, unique=True)

class Post(models.Model):
    ARTICLE = 'A'
    NEWS = 'N'
    OPTIONS = [(ARTICLE, 'Статья'), (NEWS, 'новость')]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=OPTIONS)
    time = models.DateTimeField(auto_now_add = True)
    category = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()
    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text if len(self.text) < 124 else self.text[:124] + '...'

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add = True)
    rating = models.IntegerField(default=0)
    
    def like(self):
        self.rating += 1
        self.save()
    def dislike(self):
        self.rating -= 1
        self.save()