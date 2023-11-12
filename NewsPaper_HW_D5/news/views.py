from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

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
        context['title'] = 'Новости'
        context['news_count'] = Post.objects.filter(type=Post.NEWS).count()
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class NewsSearch(ListView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news_search'
    # queryset = Post.objects.filter(type=Post.NEWS)
    paginate_by = 10

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Поиск новостей'
        context['filter'] = self.filterset
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs


class NewsDetail(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'newsDetail'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # context['full_name'] = self.object.author.user.get_full_name()
        # Переопределил метод __str__ в модели
        return context


class NewsAddView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = (
        'whiteboard.add_post',
    )
    template_name = 'news/news_add.html'
    form_class = NewsForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить новость'
        return context

    # def get_initial(self, *args, **kwargs):
    #     initial = super(NewsAddView, self).get_initial(**kwargs)
    #     initial['type'] = Post.NEWS
    #     return initial
    
    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.type = Post.NEWS
        fields.save()
        return super().form_valid(form)
    
    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         fields = form.save(commit=False)
    #         if fields.type != Post.NEWS:
    #             fields.type = Post.NEWS
    #         fields.save()
    #         form.save_m2m()
    #     return super().post(request, *args, **kwargs)


class NewsEditView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = (
        'whiteboard.change_post',
    )
    template_name = 'news/news_add.html'
    form_class = NewsForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать новость'
        return context

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = (
        'whiteboard.delete_post',
    )
    template_name = 'news/news_delete.html'
    context_object_name = 'newsDelete'
    queryset = Post.objects.all()
    success_url = reverse_lazy('news:news')
