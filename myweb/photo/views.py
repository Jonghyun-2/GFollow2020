from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.shortcuts import redirect

from .models import Photo


class PhotoUploadView(CreateView):  # CreateView 를 PhotoUploadView가 상속받는다.
    model = Photo
    fields = ['photo', 'text']
    template_name = 'photo/upload.html'  # 클래스 변수 생성, 이 변수는 실제 사용할 템플릿을 설정한다.

    def form_valid(self, form):  # 업로드를 끝내고 이동할 페이지를 호출하기 위해 사용하는 메서드
        # 이 메서드를 오버라이드해서 작성자를 설정하는 기능을 추가했다.
        # 작성자는 현재 로그인한 사용자로 설정한다.
        form.instance.author_id = self.request.user.id
        if form.is_valid():  # is_vaild() 입력 된 값들을 검증한다.
            form.instance.save()  # 이상이 없다면 데이터베이스에 저장하고
            return redirect('/')  # redirect 메서드를 이용해 메인 페이지로 이동한다.
        else:
            # 문제가 있다면 내용을 그대로 작성 페이지에 표시한다.
            return self.render_to_response({'form': form})


def photo_list(request):
    photos = Photo.objects.all()  # 데이터베이스에 저장 된 모든 사진을 불러온다.
    for a in photos.values_list():
        print(a)
    return render(request, 'photo/list.html', {'photos': photos})
# 템플릿과 뷰를 연동하기 위해서 render 함수를 사용한다.
# render 함수는 첫 번째 인자로 request
# 두 번째 인자는 랜더링 할 템플릿
# 세 번째 인자는 템플릿에 보내줄 객체나 값


class PhotoDeleteView(DeleteView):  # 제네릭 뷰 DeleteView를 사용하기 위해 상속 받는다.
    model = Photo
    success_url = '/'  # 성공 시 사이트 메인으로 이동한다.
    template_name = 'photo/delete.html'


class PhotoUpdateView(UpdateView):  # 제네릭 뷰 UpdateView를 사용하기 위해 상속 받는다.
    model = Photo
    fields = ['photo', 'text']
    template_name = 'photo/update.html'

class PhotoDiagnosisView(DetailView):  # DetailView 를 PhotoDiagnosis 상속받는다.
    model = Photo
    fields = ['photo', 'text']
    template_name = 'photo/diagnosis.html'  # 클래스 변수 생성, 이 변수는 실제 사용할 템플릿을 설정한다.