from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('create/', views.create_post, name='create_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/donate/', views.make_donation, name='make_donation'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('my-donations/', views.my_donations, name='my_donations'),
] 