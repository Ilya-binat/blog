from django.urls import path # импортирование функции path из библиотеки Django. Нужна для того что бы по определенному адресу открылась определенная страница. Стандартная функция.
from .views import * # импортирование функций из views.py. стандартная функция всегда выполняем

urlpatterns = [
    path ('', home, name = 'home'), # создали главную страницу
    path ('post/<int:pk>/', post, name = 'post'),
    path('create_post/', create_post, name = 'create_post'),
    path('post_delete/<int:pk>/', post_delete, name = 'post_delete')
]