from django.shortcuts import render,HttpResponse

# Create your views here.
def home(request):
    return render(request, r"imgupload/home.html")

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")