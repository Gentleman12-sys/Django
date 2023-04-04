from django.db import models

class User(models.Model):
    username = models.CharField('username', max_length=100)
    password = models.TextField('password', max_length=100)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Poster(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('title', max_length=50)
    content = models.TextField('content', max_length=160)
    url = models.CharField('url', max_length=1000)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'