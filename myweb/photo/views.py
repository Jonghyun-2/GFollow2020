from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.shortcuts import redirect
from django.http import HttpResponse
import json

from . import Detection
from .models import Photo
import cv2 as cv
from PIL import Image

#from .load_test_img import load_img as test


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
    #photos = Photo.objects.all()
    print("Diagnosis Called")
    fields = ['photo', 'text']
    # 클래스 변수 생성, 이 변수는 실제 사용할 템플릿을 설정한다.
    template_name = 'photo/diagnosis.html'


class PhotoPredictView(DetailView):  # DetailView 를 PhotoPredict에 상속받는다.
    model = Photo
    photos = Photo.objects.all()
    fields = ['photo', 'text']
    # 클래스 변수 생성, 이 변수는 실제 사용할 템플릿을 설정한다.
    template_name = 'photo/predict.html'


def output_view(request, pk):
    photos = Photo.objects.get(pk=pk)  # 데이터베이스에 저장 된 모든 사진을 불러온다.
    if request.is_ajax():
        print('Detection...')
        Photo_url = request.GET['Photo_url']
        Save_path = request.GET['Save_path']
        print('photo url : ', Photo_url)
        print('Save_path : ', Save_path)
        # 이미지 경로에서 /가 계속 빠짐
        # --> custom templates tag로 해결!
        img = cv.imread(Photo_url)
        #cv.imshow('test', img)
        # cv.waitKey()
        # cv.destroyAllWindows()
        model = Detection.setup()
        Detection.result(Photo_url, Save_path)

        print("Done")
        return HttpResponse(json.dumps({'paths': Photo_url}), 'application/json')
    return render(request, 'photo/predict.html', {'photos': photos})
