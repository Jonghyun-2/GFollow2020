from django.urls import path
from . import views

app_name = 'imgupload'
urlpatterns = [
    path(r"", views.home, name="home"),
    path(r"index/", views.index, name='idx'),
]
