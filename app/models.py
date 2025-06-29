from django.db import models



class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # поле автоматического добавление времени создания
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title # возвращает заголовки постов, если поставить self .body вернется тело поста
    
    def snippet(self):
        return self.body[:30] + '...'