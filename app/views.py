from django.shortcuts import render, redirect # идет по умолчанию

from django.shortcuts import get_object_or_404# Точно такой же метод получения поста из базы
#который в дополнение переведет пользователя на 404 страницу если пост не будет найден

from.models import Post, Comment

from .forms import PostForm, CommentForm

from django.http import HttpResponse

from django.contrib.auth.decorators import login_required #Декаратор - специальная функция обертка которая делает проверку
# Перед выполнение основной функции. В данном случае выполняется проверка авторизации


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
    post_detail = get_object_or_404(Post, pk=pk)
    form = CommentForm()# создали переменную form в которую передали форму для создания комментария
    return render(request, 'post.html', {'post':post_detail, 'form':form})# Для работы формы создания комментариев мы добавили GET запрос

@login_required(login_url="users:log_in")# Установили декаратор для проверки авторизации перед созданием поста
def create_post(request):
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit = False) # Вытаскиваем информацию из  формы без сохраненя в БД
        post.author=request.user # Сохраняем автором пользователя который отправил запрос
        post.save() # Сохранение поста в базе
        return redirect('app:home')
    return render(request, 'create_post.html', {'form':PostForm})

@login_required(login_url="users:log_in")
def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    if post.author != request.user:
        return render(request, '403.html')
    
    if request.method == 'POST':
        post.delete()
        return redirect('app:home')
      
    return render(request, 'post_delete.html',{'post':post})

@login_required(login_url="users:log_in")
def edit_post(request, pk):
    post = Post.objects.get(pk=pk) # поиск нужного поста в базе с помощью функции get()
    form = PostForm(request.POST or None, instance=post) # Передаем информацию поста в форму. request.POST or None
     #передается для того чтобы, мы могли увидеть форму с информацией поста и могли этот пост тут же изменить.
    if post.author != request.user:
        return render(request,'403.html') # Поставили условие, которое возвращает нас на страницу 
    #входа если пользователь пытается отредактироать не свой пост
    
    if request.method == 'POST':
        form.save()
        return redirect('app:post', pk=pk)
    return render(request, 'create_post.html', {'form':form})


def comment_create(request):
    form = CommentForm(request.POST)

    if form.is_valid():
        post_data = get_object_or_404(Post, pk=request.POST['post'])
        comment = form.save(commit=False)# приостанавливаем сохранение комментариев, чтобы указать автора и пост
        comment.author = request.user
        comment.post = post_data
        comment.save()

        return redirect('app:post', pk=request.POST['post'])
        
       
@login_required(login_url='users:log_in')
def comment_delete(request, pk):
    comment = Comment.objects.get(pk=pk)

    if request.user != comment.author:
        return render(request, '403.html')


    if request.method == 'POST':
        comment.delete()
        return redirect('app:post', pk=comment.post.pk)#достаем первичный ключ поста под которым был написан этот комментарий
    return render(request, 'comment_delete.html', {'comment':comment})



# Create your views here.

