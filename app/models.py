from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # поле автоматического добавление времени создания
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(blank=True, default = 'project_blog.png')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)# добавили поля автора для привезки его к посту 

    
    
    def __str__(self):
        return self.title # возвращает заголовки постов, если поставить self .body вернется тело поста
    
    def snippet(self):
        return self.body[:30] + '...'
    

class Comment(models.Model):
    body = models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete = models.CASCADE, default = 1)# on_delete = models.CASCADE - если удаляется пользователь, то удаляются все его записи. Эта команда создает связь с базой данных
    post = models.ForeignKey(Post, on_delete= models.CASCADE)
    is_updated = models.BooleanField(default=False)# если коментарий не отредактирован, то значение FALSE, если коментарий отредактирован, то значение меняется на FALSE. И через условие IF мы это можем показать на странице сайта
    likes = models.ManyToManyField('auth.User', related_name='comment_likes')#related_name - название 3 промежуточной промежуточной таблице в БД
    dislikes = models.ManyToManyField('auth.User', related_name='comment_dislikes')# Анаогично, как с лайками. 
    parent = models.ForeignKey('self',null=True, on_delete=models.CASCADE, related_name='children')#null=True позволяет полю в Django иметь значение NULL в базе данных, что относится к структуре базы данных, в то время как blank=True позволяет полю быть пустым при валидации в формах и является проверкой на уровне приложения, делая поле необязательным для ввода пользователем.
    reply_to = models.ForeignKey('self',null=True, on_delete=models.CASCADE, related_name='reply')#
    # parent - Это поля для сохранения id предка- первого коментария с которого началось обсуждение
    # reply_to - Поле для сохранения коментария на который пишем ответ. 

    def __str__(self):
        return self.body

    