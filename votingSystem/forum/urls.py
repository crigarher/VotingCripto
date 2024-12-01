from django.urls import path
from . import views

urlpatterns = [
    path('', views.thread_list, name='thread_list'),
    path('thread/create/', views.create_thread, name='create_thread'),
    path('thread/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('thread/<int:thread_id>/posts/', views.create_post, name='create_post'),
    path('thread/<int:thread_id>/posts/get', views.obtener_posts, name='obtener_posts'),

]
