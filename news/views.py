from django.shortcuts import render

def index(request):
    return render(request, 'news/news.html')

def new(request, pk):
    return render(request, 'news/new_page.html')