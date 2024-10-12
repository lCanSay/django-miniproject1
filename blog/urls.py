from django.urls import path
from . import views
from . import views

app_name = 'postapp'

urlpatterns = [
    path('', views.index, name = "index"),
    path('post/', views.listall, name = "listofposts"),
    path('post/<int:post_id>/', views.post_detail, name="post_detail"),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),  
]
