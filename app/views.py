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

# ORM - специальный механизм в Django, коорый предоставляет возможность писать python код,
# для рботы с базой данных 

# get() - вернет первый подходящий элемент
# filter() - вернет все элементы которые подходят по условию 

def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {'posts':posts}) #  Функция открытия нашей стратовой транице


def post(request, pk):
    post_detail = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post = pk, parent = None)
    form = CommentForm()# создали переменную form в которую передали форму для создания комментария
    return render(request, 'post.html', {'post':post_detail, 'form':form, 'comments':comments})# Для работы формы создания комментариев мы добавили GET запрос

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
     #inctance - отвечает за отображние текста который в него передается
    if post.author != request.user:
        return redirect('users:log_in') # Поставили условие, которое возвращает нас на страницу 
    #входа если пользователь пытается отредактироать не свой пост
    
    if request.method == 'POST':
        form.save()
        return redirect('app:post', pk=pk)
    return render(request, 'create_post.html', {'form':form})

@login_required(login_url="users:log_in")
def comment_create(request):
    form = CommentForm(request.POST)

    if form.is_valid():
        post_data = get_object_or_404(Post, pk=request.POST['post'])
        comment = form.save(commit=False)#commit=False - приостанавливает сохранение данных с формы, для того чтобы дополнить информацию автором и постом под которым пишется комментарий
        comment.author = request.user
        comment.post = post_data
        comment.save()

        return redirect('app:post', pk=request.POST['post'])
    

@login_required(login_url='users:log_in')
def comment_delete(request, pk):
    comment = Comment.objects.get(pk=pk)

    if request.method=='POST':
        comment.delete()

        return redirect('app:post', pk=comment.post.pk)#pk=comment.post.pk - из коментария достаем его пост. А если написать pk = pk, то мы говорим что первичный ключ поста = первичному посту коментария, а это не так.
        


@login_required(login_url='users:log_in')
def comment_like(request, pk):
    comment = Comment.objects.get(pk=pk)

    if request.user not in comment.likes.all():
        comment.likes.add(request.user)
        comment.dislikes.remove(request.user)

    elif request.user in comment.likes.all():
        comment.likes.remove(request.user)
    


    return redirect('app:post', pk = comment.post.pk)

@login_required(login_url='users:log_in')
def comment_dislike(request, pk):
    comment = Comment.objects.get(pk=pk)

    if request.user not in comment.dislikes.all():
        comment.dislikes.add(request.user)
        comment.likes.remove(request.user)

    elif request.user in comment.dislikes.all():
        comment.dislikes.remove(request.user)

    return redirect('app:post', pk = comment.post.pk)

@login_required(login_url='users:log_in')
def comment_edit(request, pk):
  
    comment = Comment.objects.get(pk=pk)
    form = CommentForm(request.POST or None, instance=comment)

    if comment.author != request.user:
        return render(request, '403.html')

    if form.is_valid():
        form.save()

    return redirect('app:post', pk = comment.post.pk)  
 
@login_required(login_url='users:log_in')
def comment_reply(request, pk):
    
    comment = Comment.objects.get(pk = pk)
    form = CommentForm(request.POST or None)
   
    if form.is_valid():
        if comment.parent is None:
            parent_comment = comment
        else:
            parent_comment = comment.parent
        
        reply_to = comment
        instance = form.save(commit=False)
        instance.parent = parent_comment
        instance.reply_to = reply_to
        instance.post = parent_comment.post
        instance.author = request.user
        instance.save()

    return redirect('app:post', pk = comment.post.pk)     
    

    
  
  



# POST запрос - подрузомевает сздание новой информации




