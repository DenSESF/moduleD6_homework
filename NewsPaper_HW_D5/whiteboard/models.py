from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.urls import reverse_lazy


class Author(models.Model):
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        self.rating = 0
        if self.post_set.filter(type=Post.ARTICLE).exists():
            allArticle = self.post_set.filter(type=Post.ARTICLE)
            self.rating = allArticle.aggregate(rSum=Sum('rating')).get('rSum') * 3
            allCommentArticle = Comment.objects.filter(post__in=allArticle)
            self.rating += allCommentArticle.aggregate(rSum=Sum('rating')).get('rSum')
        if self.user.comment_set.all().exists():
            self.rating += self.user.comment_set.all().aggregate(rSum=Sum('rating')).get('rSum')
        self.save()
    
    def __str__(self):
        return self.user.get_full_name()


class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    ARTICLE = 'A'
    NEWS = 'N'
    OPTIONS = [(ARTICLE, 'Статья'), (NEWS, 'Новость')]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=OPTIONS)
    time = models.DateTimeField(auto_now_add = True)
    category = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    # def __str__(self):
    #     return self.header

    def like(self):
        self.rating += 1
        self.save()
    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text if len(self.text) < 124 else self.text[:124] + '...'
    
    def get_absolute_url(self):
        # return f'/news/{self.id}'
        return reverse_lazy('news:news_view', args=[str(self.pk)])

    
    class Meta:
        ordering = ('-time',)


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
