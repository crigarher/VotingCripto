from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('index', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('thread/<int:thread_id>/create_poll/', views.create_poll, name='create_poll'),
    path('results/<int:question_id>/pdf/', views.generate_pdf, name='generate_pdf'),
]