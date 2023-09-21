from django.urls import path

from news.views import index, new

app_name = 'news'

urlpatterns = [
    path('', index, name='news'),
    path('<int:pk> ', new, name='one_new'),
]

