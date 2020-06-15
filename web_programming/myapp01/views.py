from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def upload_img(request):
    return render(request, 'Image upload.html')