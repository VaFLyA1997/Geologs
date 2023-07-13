from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='index'),
    path('news/', views.news),
    path('news/<int:pk>/', views.newsSingle, name='newsSingle'),
    path('documents/', views.docs),
    path('filter_documents/', views.filter_documents, name='filter_documents'),
    path('contacts/', views.contacts),
    path('download/<int:pk>/', views.download, name='download'),
    path('forum/', views.forum, name='forum'),
    path('forum/<int:forum_id>/', views.single_forum, name='singleForum'),
    path('vote/', views.vote, name='vote'),
    path('login/', views.handle_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('profile/<int:id>', views.profile, name='profile'),
    path('voted/<int:forum_id>/', views.voted_users, name='voted_users'),
]