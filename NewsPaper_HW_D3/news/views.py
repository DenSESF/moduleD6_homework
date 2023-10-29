# from django.shortcuts import render
from typing import Any
from django.views.generic import ListView, DetailView
from whiteboard.models import Post
# from datetime import datetime
from django.utils import timezone

# Create your views here.

class NewsList(ListView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news'
    # queryset = Post.objects.filter(type=Post.NEWS).order_by('-time')
    # перенес сортировку по убыванию в модели
    queryset = Post.objects.filter(type=Post.NEWS)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['time_now'] = timezone.localtime(timezone.now())
        context['title'] = 'Новости'
        return context

class NewsDetail(DetailView):
    model = Post
    template_name = 'news/newsdetail.html'
    context_object_name = 'newsDetail'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # context['full_name'] = self.object.author.user.get_full_name()
        # Переопределил метод __str__ в модели
        context['full_name'] = self.object.author
        return context
