from django.contrib import admin
from django.urls import path, include # include - соединяет два роутера (соединяет app c нашим проектом)
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404 #Функция которая показывает страницу 404 по умолчанию
from django.shortcuts import render

def custom_404(request, exception):
    return render(request, '404.html', status=404) #Кастомная функция которая показывает 
# Подготовленную странницу 404
handler404=custom_404

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("app.urls", "app"), namespace="app")),
    path("users/", include(("users.urls", "users"), namespace = "users"))
]
urlpatterns += staticfiles_urlpatterns() # Встроенная в  django функция которая найдет в settings.py адресс папки со статичными файлами 
#и настроит открытие этих файлов через браузер. 

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)