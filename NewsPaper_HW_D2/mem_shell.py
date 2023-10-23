# Создать двух пользователей (с помощью метода User.objects.create_user).
from django.contrib.auth.models import User
user1 = User.objects.create_user('user1', 'user1@example.com', 'secret1')
user2 = User.objects.create_user('user2', 'user2@example.com', 'secret2')

# Создать два объекта модели Author, связанные с пользователями.
from whiteboard.models import *
author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)

# Добавить 4 категории в модель Category.
cat1 = Category.objects.create(name='категория 1')
cat2 = Category.objects.create(name='категория 2')
cat3 = Category.objects.create(name='категория 3')
cat4 = Category.objects.create(name='категория 4')

# Добавить 2 статьи и 1 новость.
text1 = 'A' * 124 + 'B' * 10
news1 = Post.objects.create(author=author1, type=Post.NEWS, header='News one', text=text1)
text1 = 'B' * 124 + 'c' * 10
article1 = Post.objects.create(author=author1, type=Post.ARTICLE, header='Article one', text=text1)
text1 = 'C' * 124 + 'd' * 10
article2 = Post.objects.create(author=author2, type=Post.ARTICLE, header='Article two', text=text1)

# Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
news1.category.add(cat1, cat2)
article1.category.add(cat3)
article2.category.add(cat4)

# отключили свет :(

from django.contrib.auth.models import User
from whiteboard.models import *

user1 = User.objects.get(username='user1')
user2 = User.objects.get(username='user2')
cat1 = Category.objects.get(id=1)
cat3 = Category.objects.get(id=3)
cat4 = Category.objects.get(id=4)
article1 = Post.objects.get(category=cat3)
article2 = Post.objects.get(category=cat4)

# Создать как минимум 4 комментария к разным объектам модели Post
# (в каждом объекте должен быть как минимум один комментарий).
com1 = Comment.objects.create(post=news1, user=user1, text='Комментарий 1')
com2 = Comment.objects.create(post=news1, user=user2, text='Комментарий 2')
com3 = Comment.objects.create(post=article1, user=user2, text='Комментарий 3')
com4 = Comment.objects.create(post=article2, user=user2, text='Комментарий 4')

# Применяя функции like() и dislike() к статьям/новостям и комментариям,
# скорректировать рейтинги этих объектов.
news1.like()
news1.like()
news1.like()
news1.dislike()
com1.like()
com1.like()
com1.like()
com1.like()
com2.dislike() 
com2.dislike()
com2.dislike()
com2.dislike()
com2.dislike()
com2.dislike()
com2.dislike()
com3.dislike() 
com3.dislike()
com3.dislike()
com3.like()    
com3.like()
com3.like()
com3.like()
com3.like()
com4.like()
article1.like()
article1.like()
article1.like()
article1.like()
article1.like()
article1.like()
article1.like()
article1.dislike()
article2.dislike()
article2.dislike()
article2.dislike()
article2.dislike()

# Обновить рейтинги пользователей.
author1 = Author.objects.get(user=user1)
author1.update_rating()

author2 = Author.objects.get(user=user2)
author2.update_rating()

# Вывести username и рейтинг лучшего пользователя
# (применяя сортировку и возвращая поля первого объекта).
Author.objects.all().order_by('-rating').values('user__username', 'rating')[0]

#Вывести дату добавления, username автора, рейтинг,
# заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
best_article = Post.objects.filter(type=Post.ARTICLE).order_by('-rating')[0]
print(best_article.time, best_article.author.user.username, best_article.rating, best_article.header, best_article.preview())

# Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
Comment.objects.filter(post=best_article).values('time', 'user__username', 'rating', 'text')
