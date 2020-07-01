from django.conf.urls import url

from . import views

app_name = 'ajax'
urlpatterns = [
    url(r'', views.ajaxTest, name='post_list'),

]
