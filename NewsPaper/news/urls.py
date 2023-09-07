# from django import views
from django.urls import path
from .views import NewsList, NewsDetail, LoremDetail, PostDelete, PostSearch, SearchHeader, AddPost, PostUpdate, CategoryNewsView, post_limit, subscribe_category, unsubscribe_category
from django.views.decorators.cache import cache_page

# app_name ='news'
urlpatterns = [
    path('', cache_page(60)(NewsList.as_view()), name='news'),
    path('<int:pk>/', LoremDetail.as_view(), name='lorem_post'),
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('search_site/', PostSearch.as_view(), name='search_site'),
    path('search_2/', SearchHeader.as_view(), name='search_2'),
    path('post_limit/', post_limit, name='post_limit'),
    path('add_post/', AddPost.as_view(), name='add_post'),
    path('<int:pk>/edit_post/', PostUpdate.as_view(), name='edit_post'),
    path('<int:pk>/delete_post/', PostDelete.as_view(), name='delete_post'),
    # ================================
    path('category/<int:category_id>/', CategoryNewsView.as_view(), name='category'),
    path('subscribe/<int:category_id>/', subscribe_category, name='subscribe'),
    path('unsubscribe/<int:category_id>/', unsubscribe_category, name='unsubscribe'),
    ]

