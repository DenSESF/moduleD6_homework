from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.urls import reverse_lazy

from typing import Any

from whiteboard.models import Post
from .filters import NewsFilter
from .forms import NewsForm


class NewsList(ListView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news'
    # queryset = Post.objects.filter(type=Post.NEWS).order_by('-time')
    # ordering = ['-time']
    # перенес сортировку по убыванию даты в модели
    queryset = Post.objects.filter(type=Post.NEWS)
    paginate_by = 10

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['time_now'] = timezone.localtime(timezone.now())
        context['title'] = 'Новости'
        context['news_count'] = Post.objects.filter(type=Post.NEWS).count()
        return context


class NewsSearch(ListView):
    model = Post
    template_name = 'news/news.html'
    #queryset = Post.objects.filter(type=Post.NEWS)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['time_now'] = timezone.localtime(timezone.now())
        context['title'] = 'Поиск новостей'
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        # context['filter'] = NewsFilter(self.request.GET, queryset=self.queryset)
        # context['choices'] = Product.TYPE_CHOICES
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'newsDetail'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # context['full_name'] = self.object.author.user.get_full_name()
        # Переопределил метод __str__ в модели
        return context


class NewsAddView(CreateView):
    template_name = 'news/news_add.html'
    form_class = NewsForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить новость'
        return context

    def get_initial(self, *args, **kwargs):
        initial = super(NewsAddView, self).get_initial(**kwargs)
        initial['type'] = Post.NEWS
        return initial


class NewsEditView(UpdateView):
    template_name = 'news/news_add.html'
    form_class = NewsForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать новость'
        return context

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDeleteView(DeleteView):
    template_name = 'news/news_delete.html'
    context_object_name = 'newsDelete'
    queryset = Post.objects.all()
    success_url = reverse_lazy('news:news')
