from django.shortcuts import render, redirect # идет по умолчанию

from.models import Post

from .forms import PostForm


# GET запрос - нужен только для вывода информации. на пример вытащить список постов или один пост

# POST запрос - нужен для внесения, или изменения, или удаления какой-либо информации

# render() - Выполняет подготовку html ответа на запрос пользователя. Отлавливается запрос
# Собирается вся нужная информация с базы и передается в html шаблон

# redirect() - В свою очередь передает выполнение другому представлению(функции)
#Функция redirect() перенаправляет пользователя на другую страницу. И для отрисовки этой странице сработает 
#соответсвующая функция

# На пример: После создания нового поста пользователь должен быть перенаправлен на
#главную страницу, чтобы увидеть только что созданный пост
# Все что касается создания поста выполняет функция создания поста, а когда происходит перенаправление пользователя
# То срабатывает функция home()
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

def edit_post(request, pk):
    post = Post.objects.get(pk=pk) # поиск нужного поста в базе с помощью функции get()
    form = PostForm(request.POST or None, instance=post) # Передаем информацию поста в форму. request.POST or None
     #передается для того чтобы, мы могли увидеть форму с информацией поста и могли этот пост тут же изменить.
    
    if request.method == 'POST':
        form.save()
        return redirect('app:post', pk=pk)
    return render(request, 'create_post.html', {'form':form})



# Create your views here.

