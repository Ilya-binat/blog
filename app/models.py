from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # поле автоматического добавление времени создания
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(blank=True, default = 'project_blog.png')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)# добавили поля автора для привезки его к посту 
    likes = models.ManyToManyField('auth.User', related_name='post_likes')
    dislikes = models.ManyToManyField('auth.User', related_name = 'post_dislikes')
    
    
    def __str__(self):
        return self.title # возвращает заголовки постов, если поставить self .body вернется тело поста
    
    def snippet(self):
        return self.body[:30] + '...'
    

class Comment(models.Model):
    body = models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)# DateTimeField Сохраняет при добавление комментария дату и время. 
    author = models.ForeignKey(User, on_delete = models.CASCADE, default = 1)
    post = models.ForeignKey(Post, on_delete= models.CASCADE)
    is_updated = models.BooleanField(default = False)
    likes = models.ManyToManyField('auth.User', related_name='comment_likes')
    dislikes = models.ManyToManyField('auth.User', related_name = 'comment_dislikes')
    parent = models.ForeignKey('self', null = True, blank = True, related_name = 'reply', on_delete = models.CASCADE)# поле в котором сохраниться ID родительского комментария
# self - обозначает обращение к самой же модели комментария включая все поля 
# null = True - Обозначает, что поле не обязательное, то есть может быть пустым в базе данных  
#blank = True - Обозначает, что поле не обязательное при заполнение форм 
# null = True - это настройка на уровне базы данных
# blank = True - это настройка на уровне формы
#related_name = 'reply' - Обращение к ответам комментраиев 
# on_delete = models. CASCSDE - Означает, если удалился родительский комментарий, то удаляются все его ответы 
#
#

    def __str__(self):
        return self.body

    