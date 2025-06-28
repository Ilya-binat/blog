from django.shortcuts import render # идет по умолчанию


def home(request):
    return render(request, 'home.html') #  Функция открытия нашей стратовой транице
# Create your views here.
