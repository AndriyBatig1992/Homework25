from django.urls import path
from . import views


app_name = "quotes"

urlpatterns = [
    path('', views.main, name='root'),
    path('<int:page>', views.main, name='root_paginate'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('add_tag/', views.add_tag, name='add_tag'),
    path('add_author/', views.add_author, name='add_author'),
    path('author_detail/<int:author_id>/', views.author_detail, name='author_detail'),
    path('tag_detail/<int:tag_id>/', views.tag_detail, name='tag_detail'),
    path('quote_detail/<int:quote_id>', views.quote_detail, name='quote_detail'),
    path('delete_quote/<int:quote_id>/', views.delete_quote, name='delete_quote'),
    path('edit_quote/<int:quote_id>/', views.edit_quote, name='edit_quote'),
    path('upload/', views.upload, name='upload'),
    path("pictures/", views.pictures, name='pictures'),
    path("edit_picture/<int:pic_id>", views.edit_picture, name='edit_picture'),
    path("remove_picture/<int:pic_id>", views.remove_picture, name='remove_picture'),
]
