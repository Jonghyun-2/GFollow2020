from django.contrib import admin
from .models import Question,Choice
# Register your models here.
class ChoiceInline(admin.TabularInline):
    # Choice 모델을 Qusetion 내부에서 볼 수 있도록 설계
    model = Choice
    # 입력되지 않은 여유분(공백)을 2개 보여줌
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Question Statement", {"fields" : ["Q_text"]}),
        ("Data Info", {"fields":['pub_date'],'classes':['collapse']}),
    ]
    inlines = [ChoiceInline]  # Choice모델 클래스 같이보기
    list_display = ("Q_text", 'pub_date')  # list 최상단에 출력되는 메시지
    list_filter = ["Q_text",'pub_date']
    search_fields = ["Q_text"]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)