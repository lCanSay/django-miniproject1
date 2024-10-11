from django.urls import path
from . import views

app_name = 'postapp'

urlpatterns = [
    path('', views.index, name = "index"),
    path('post/', views.listall, name = "listofposts"),
    path('post/<int:id>/', views.post_detail, name="post_detail"),
]
