from django.urls import path
from . import views

urlpatterns = [
    path('stock/movement/<str:article_id>/', views.article_movement, name='article_movement'),
    path('stock/movement/', views.article_movement, name='article_movement'),
]