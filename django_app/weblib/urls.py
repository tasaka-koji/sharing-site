from django.urls import path
from . import views

urlpatterns = [
    #v1
    path('', views.index, name='index'),
    path('<int:page>', views.index, name='index'),
    path('mypage', views.mypage, name='mypage'),
    path('mypage/<int:page>', views.mypage, name='mypage'),
    path('make_tag', views.make_tag, name='make_tag'),
    path('make_tagarrow/<int:article_id>', views.make_tagarrow, name='make_tagarrow'),
    path('post', views.post, name='post'),
    path('detail/<int:article_id>', views.detail, name='detail'),
    path('edit/<int:article_id>', views.edit, name='edit'),
    path('delete/<int:article_id>', views.delete, name='delete'),
    path('delete_comment/<int:comment_id>', views.delete_comment, name='delete_comment'),
    #path('', views.index, name='index'),
    
]