from django.shortcuts import render, redirect # идет по умолчанию

from.models import Post

from .forms import PostForm

def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {'posts':posts}) #  Функция открытия нашей стратовой транице


def post(request, pk):
    post_detail = Post.objects.get(pk=pk)
    return render(request, 'post.html', {'post':post_detail})


def create_post(request):
    form = PostForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('app:home')
    return render(request, 'create_post.html', {'form':PostForm})

def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('app:home')
      
    return render(request, 'post_delete.html',{'post':post})



# Create your views here.

