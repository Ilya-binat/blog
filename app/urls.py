from django.urls import path # импортирование функции path из библиотеки Django. Нужна для того что бы по определенному адресу открылась определенная страница. Стандартная функция.
from .views import * # импортирование функций из views.py. стандартная функция всегда выполняем

urlpatterns = [
    path ('', home, name = 'home'), # создали главную страницу
    path ('post/<int:pk>/', post, name = 'post'),
    path('create_post/', create_post, name = 'create_post'),
    path('post_delete/<int:pk>/', post_delete, name = 'post_delete'),
    path('edit_post/<int:pk>/', edit_post, name = 'edit_post'),
    path('comment_create/', comment_create, name = 'comment_create'),
    path('comment_delete/<int:pk>', comment_delete, name = 'comment_delete'),
    path('comment_edit/<int:pk>', comment_edit, name = 'comment_edit'),
    path('post_like/<int:pk>', post_like, name = 'post_like'),
    path('post_dislike/<int:pk>', post_dislike, name ='post_dislike')
]