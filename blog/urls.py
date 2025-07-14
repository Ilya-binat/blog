from django.contrib import admin
from django.urls import path, include # include - соединяет два роутера (соединяет app c нашим проектом)
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("app.urls", "app"), namespace="app")),
]
urlpatterns += staticfiles_urlpatterns() # Встроенная в  django функция которая найдет в settings.py адресс папки со статичными файлами 
#и настроит открытие этих файлов через браузер. 

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)