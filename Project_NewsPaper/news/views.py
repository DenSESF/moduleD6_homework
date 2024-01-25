# flake8: noqa E501
# from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
# from django.views.defaults import page_not_found
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)

from whiteboard.models import Post, Author, Category, SubscriberUser
from .filters import NewsFilter
from .forms import NewsForm

from django.utils import timezone

from NoticesTasks.scheduler import bg_notice_create_new_post


class NewsList(ListView):
    # model = Post
    template_name = 'news/news.html'
    context_object_name = 'news'
    # queryset = Post.objects.filter(type=Post.NEWS).order_by('-time')
    # ordering = ['-time']
    # перенес сортировку по убыванию даты в модели
    queryset = Post.objects.filter(type=Post.NEWS)
    # queryset = Post.objects.filter(type=Post.NEWS).prefetch_related('category')
    # queryset = Post.objects.prefetch_related('category').filter(type=Post.NEWS)
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новости'
        # не нужно, использовал paginator.count в шаблоне
        # context['news_count'] = self.get_queryset().count()
        context['is_subscriber'] = False
        # context['category_list'] = \
        #     self.get_queryset().order_by('category').values_list('category', 'category__name').distinct()
        context['category_list'] = Category.objects.values_list('id', 'name')
        user = self.request.user
        cat_id = self.request.GET.get('cat')
        if cat_id is None:
            context['all_news_radio'] = 'checked'
        elif cat_id.isnumeric():
            context['all_news_radio'] = 'disabled'
            context['current_category_id'] = int(cat_id)
            if user.is_authenticated:
            #     context['is_subscriber'] = \
            #         self.get_queryset().filter(
            #         category=cat_id,
            #         category__subscribers=user
            #     ).exists()
                context['is_subscriber'] = \
                    SubscriberUser.objects.filter(
                        user=user,
                        category=cat_id
                    ).exists()
        context['is_not_author'] = \
            not self.request.user.groups.filter(name='authors').exists()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        cat_id = self.request.GET.get('cat')
        if cat_id is None:
            return queryset
        if cat_id.isnumeric():
            return queryset.filter(category=cat_id)
        return queryset.none()
    
    # def get(self, request, *args, **kwargs):
    #     cat_id = self.request.GET.get('cat')
    #     if cat_id is None or cat_id.isnumeric():
    #         return super().get(request, *args, **kwargs)
    #     return page_not_found(request, ObjectDoesNotExist())
        

class NewsSearch(ListView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news_search'
    # queryset = Post.objects.filter(type=Post.NEWS)
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Поиск новостей'
        context['filter'] = self.filterset
        context['is_not_author'] = \
            not self.request.user.groups.filter(name='authors').exists()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs


class NewsDetail(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'newsDetail'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['full_name'] = self.object.author.user.get_full_name()
    #     Переопределил метод __str__ в модели
    #     return context


class NewsAddView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = (
        'whiteboard.add_post',
    )
    template_name = 'news/news_add.html'
    form_class = NewsForm

    def get(self, request: HttpRequest, *args: str, **kwargs):
        if Author.objects.filter(user=request.user).exists():
            author = Author.objects.get(user=self.request.user)
            today_day = timezone.now().day
            count_post = Post.objects.filter(
                time__day=today_day,
                author=author,
                type=Post.NEWS,
            ).count()
            if count_post == 3:
                return \
                    HttpResponseRedirect(reverse_lazy('news:news_qty_exced'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить новость'
        return context

    # def get_initial(self, *args, **kwargs):
    #     initial = super(NewsAddView, self).get_initial(**kwargs)
    #     initial['type'] = Post.NEWS
    #     return initial

    def form_valid(self, form):
        fields = form.save(commit=False)
        if Author.objects.filter(user=self.request.user).exists():
            fields.author = Author.objects.get(user=self.request.user)
        else:
            fields.author = Author.objects.create(user=self.request.user)
        fields.type = Post.NEWS
        fields.save()
        form.save_m2m()
        '''
        Запуск задачи на отправку уведомлений о создании новой новости.
        Сигнал post_save не получает связи с таблицей подписчиков категорий
        т.к. она еще не создана.
        Сигнал m2m_change срабатывает при любом изменении полей категории,
        невозможно понять пост только создан или же он уже существовал.
        поэтому реализация в виде фонового планировщика.
        '''
        bg_notice_create_new_post(fields)
        return HttpResponseRedirect(fields.get_absolute_url())

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         fields = form.save(commit=False)
    #         if fields.type != Post.NEWS:
    #             fields.type = Post.NEWS
    #         fields.save()
    #         form.save_m2m()
    #     return super().post(request, *args, **kwargs)


class NewsQtyExceeded(TemplateView):
    template_name = 'news/news_qty_exceeded.html'


class NewsEditView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = (
        'whiteboard.change_post',
    )
    template_name = 'news/news_add.html'
    form_class = NewsForm

    def get_context_data(self, **kwargs):
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
