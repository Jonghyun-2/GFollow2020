from django.urls import path
from polls import views

app_name = 'polls'
urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'<int:question_id>/', views.detail, name='detail'),
    path(r'<int:question_id>/result', views.result, name='result'),
    path(r'<int:question_id>/vote', views.vote, name='vote'),
]