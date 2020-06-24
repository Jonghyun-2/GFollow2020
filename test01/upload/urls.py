from django.urls import path
from upload import views

app_name = 'upload'
urlpatterns = [
    path(r'', views.upload_file,name='home'),
    path(r'success/', views.success, name='success'),
]

