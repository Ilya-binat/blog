from django.shortcuts import render # идет по умолчанию

from.models import Post


def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {'posts':posts}) #  Функция открытия нашей стратовой транице


# Create your views here.

