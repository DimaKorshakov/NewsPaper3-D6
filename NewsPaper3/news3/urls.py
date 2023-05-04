from django.urls import path
from .views import IndexView

from .views import NewsList, Search, NewsDetailView, NewsCreateView, NewsUpdateView, NewsDeleteView, CategoryView, \
    CatsView, SubscribeToCategory, UnSubscribeToCategory  # импортируем наше представление

urlpatterns = [

    path('', IndexView.as_view()),
    path('news/', NewsList.as_view()),
    path('news/search/', Search.as_view()),
    path('<int:pk>/', NewsDetailView.as_view(), name='news_detail'),  # Ссылка на детали товара
    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('update/<int:pk>', NewsUpdateView.as_view(), name='news_update'),
    path('delete/<int:pk>', NewsDeleteView.as_view(), name='news_delete'),
    path('news/category/', CategoryView.as_view(), name='category'),
    path('news/category/<int:pk>', CatsView.as_view(), name='cats'),
    path('news/category/<int:pk>/subscribe/', SubscribeToCategory.as_view(), name='subscribe'),
    path('news/category/<int:pk>/unsubscribe/', UnSubscribeToCategory.as_view(), name='unsubscribe'),
]
