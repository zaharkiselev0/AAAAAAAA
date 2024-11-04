from django.db import models
from django.contrib.auth.models import User

from news_app.models import *

users = User.objects.bulk_create((User(username=name) for name in ["Василий", "Колян"]))
pusers = Puser.objects.bulk_create((Puser(user=u) for u in users))

vasya, kolya = Author.objects.bulk_create((Author(puser=p) for p in pusers))

science, entertainments, sport, business = Category.objects.bulk_create(
    (Category(category=c) for c in ["Наука", "Развлечения", "Спорт", "Бизнес"]))

posts_keys = ['author', 'article', 'title', 'text']
posts_params = [[vasya, True, 'статья 1', 'текст статьи 1'],
                [vasya, False, 'статья 2', 'текст статьи 2'],
                [kolya, True, 'статья 3', 'текст статьи 3'],]
post1, post2, post3 = Post.objects.bulk_create((Post(**dict(zip(posts_keys, params))) for params in posts_params))


Postcategory_lst = []
for post, categories in zip([post1, post2, post3], [[science], [business], [sport, entertainments]]):
    for category in categories:
        Postcategory_lst.append(PostCategory(post=post, category=category))
PostCategory.objects.bulk_create(Postcategory_lst)

comments_keys = ['post', 'puser', 'text']
comments_params = [[post1, kolya.puser, 'Очень интересная статья от Васи'],
                   [post1, vasya.puser, 'Очень интересная статья от Меня'],
                   [post2, kolya.puser, 'puser.user.username...'],
                   [post3, vasya.puser, 'ыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыы'],]
comments = Comment.objects.bulk_create(
    (Comment(**dict(zip(comments_keys, params))) for params in comments_params))

for comment, likes in zip(comments, [10, 5, 13, 8]):
    for _ in range(likes):
        comment.like()
    comment.save()

for post, likes in zip(Post.objects.all(), [15, 20, 9]):
    for _ in range(likes):
        post.like()
    post.save()

for puser in Puser.objects.all():
    puser.update_rating()
    puser.save()

best_user = Puser.objects.order_by('-rating').first()
print(f"лучший пользователь: {best_user.user.username}, рейтинг: {best_user.rating}")

best_post = Post.objects.order_by('-rating').first()
print(f"лучший пост: {best_post.title}, рейтинг: {best_user.rating}, автор: {best_post.author.puser.user.username},"
      f"дата добавления: {best_post.date}, превью: {best_post.preview()}")

print("Комменты к лучшей статье:")
print(*best_post.comment_set.values_list('text', flat=True), end='\n')


