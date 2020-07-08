from django.shortcuts import render

from django.views.generic.edit import CreateView

from django.contrib.auth.forms import UserCreationForm

from django.http import HttpResponse

import json
from .test import print_hello
import cv2 as cv


# def ajaxTest(request):

#     if request.is_ajax():

#         data = request.GET['click']
#         # sth function
#         # ex print_hello

#         # 이미지 입력
#         # 이미지의 URL로 입력 받음
#         img = cv.imread(r'E:\Input_test\test.jpg')

#         # 딥러닝 모델을 통한 결과 측정
#         # pred = model_predict_value(img)

#         # 이미지 출력
#         cv.imwrite(r'E:\Output_test\output.jpg', img)
#         # message(key) , data(value)
#         return HttpResponse(json.dumps({'message': data}), 'application/json')

#     return render(request, 'ajaxtest.html')

def ajaxTest(request):
    print("ajaxTest called")
    if request.is_ajax():

        data = request.GET['click']
        print(data)
        print("requset func called")
        # sth function
        # ex print_hello

        # 이미지 입력
        # 이미지의 URL로 입력 받음
        #img = cv.imread(r'E:\Input_test\test.jpg')

        # 딥러닝 모델을 통한 결과 측정
        # pred = model_predict_value(img)

        # 이미지 출력
        #cv.imwrite(r'E:\Output_test\output.jpg', img)
        # message(key) , data(value)
        return HttpResponse(json.dumps({'paths': data}), 'application/json')

    return render(request, 'ajaxtest.html')
