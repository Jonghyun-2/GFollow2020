from django.urls import path
from django.views.generic.detail import DetailView

from .views import *
from .models import Photo

app_name = 'photo'  # 네임스페이스로 사용되는 값이다.
# 템플릿에서 url 템플릿 태그를 사용할 때 app_name 값이 설정되어 있다면
# [app_name:URL패턴이름] 형태로 사용한다.
urlpatterns = [
    path('', photo_list, name='photo_list'),  # 함수형(def) 뷰
    path('detail/<int:pk>/', DetailView.as_view(model=Photo,
                                                template_name='photo/detail.html'), name='photo_detail'),
    # 제네릭 뷰를 그대로 사용하는 인라인 뷰
    # urls.py 에서 인라인 코드로 작성할 수 있습니다. path 함수에 인수로 전달할 때는
    # as_view안에 클래스 변수들을 설정해 사용합니다.
    path('upload/', PhotoUploadView.as_view(), name='photo_upload'),
    path('delete/<int:pk>/', PhotoDeleteView.as_view(), name='photo_delete'),
    path('update/<int:pk>/', PhotoUpdateView.as_view(), name='photo_update'),
    # 함수 형 뷰는 뷰 이름만 써주고 클래스(class) 형 뷰는 뒤에 .as_view()를 붙인다.
]
