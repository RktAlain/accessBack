from django.urls import path
from . import views

urlpatterns = [
    path('articlescreate/', views.article_view, name='article_view'),
    path('article/', views.article_view, name='article_liste'),
    path('article/<str:article_id>', views.article_view, name='article_detail'),
    # path('articles/movement/<str:article_id>/', views.article_movement, name='article_movement'),
]