from django.shortcuts import render, redirect # идет по умолчанию

from.models import Post



def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {'posts':posts}) #  Функция открытия нашей стратовой транице


def post(request, pk):
    post_detail = Post.objects.get(pk=pk)
    return render(request, 'post.html', {'post':post_detail})






# Create your views here.

