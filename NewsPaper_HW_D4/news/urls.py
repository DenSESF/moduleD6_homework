from django.urls import path
from .views import NewsList, NewsDetail, NewsSearch, NewsAddView, NewsEditView, NewsDeleteView


app_name = 'news'
urlpatterns = [
    path('', NewsList.as_view(), name='news'),
    path('<int:pk>', NewsDetail.as_view()),

    path('search/', NewsSearch.as_view()),

    path('add/', NewsAddView.as_view(), name='news_add'),
    path('<int:pk>/edit/', NewsEditView.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
]
