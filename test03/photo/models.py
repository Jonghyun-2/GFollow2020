from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User  # 가져온 User를 class Photo 에서 사용


class Photo(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_photos')
    # ForeignKey를 사용하여 User 테이블과 관계를 만듭니다. 여기서 User 모델은 장고에서 기본적으로 사용하는
    # 사용자 모델입니다. on_delete 인수는 연결된 모델이 삭제될 경우 현재 모델의 값은 어떻게 할 것이냐 이다.
    '''
    CASCADE : 연결된 객체가 지워지면 해당 하위 객체도 같이 삭제
    PROTECT : 하위 객체가 남아 있다면 연결된 객체가 지워지지 않음
    SET_NULL : 연결된 객체만 삭제하고 필드 값을 NULL로 설정
    SET_DEFAULT : 연결된 객체만 삭제하고 필드 값을 설정된 기본 값으로 변경
    SET() : 연결된 객체만 삭제하고 지정한 값으로 변경
    DO_NOTHING : 아무 일도 하지 않음
    '''
    # 세 번째 인수인 related_name 은 연결된 객체에서 하위 객체의 목록을 부를 때 사용할 이름이다.
    # Photo 모델을 예로 들면 어떤 유저가 작성한 글을 불러 올 때는 유저 객체에 user_photos 속성을 참조하면 된다.
    photo = models.ImageField(upload_to=r'./photos',
                              default=r'photos/no_image.png')
    # upload_to 는 사진이 업로드 될 경로를 설정한다. 만약 업로드가 되지 않을 경우 default 값으로 대체.
    text = models.TextField()
    # 텍스트 필드, 문자열 길이 제한 X
    created = models.DateTimeField(auto_now_add=True)
    # 글 작성 일을 저장하기 위한 날짜시간 필드
    # auto_now_add 옵션을 설정하면 객체가 추가될 때 자동으로 값을 설정한다.
    # 한마디로 게시글이 작성될 때의 시간을 갖고 upload_to 의 경로에 맞게끔 값을 넣어준다.
    updated = models.DateTimeField(auto_now=True)
    # 글 수정 일을 저장하기 위한 날짜시간 필드이다. auto_now 옵션을 설정하면 객체가 수정 될 때 마다 자동으로 값을 설정한다.

    class Meta:  # 옵션 클래스
        ordering = ['-updated']
    # ordering 클래스 변수는 해당 모델의 객체들을 어떤 기준으로 정렬할 것인지 설정하는 옵션
    # -updated 로 설정했으니 글 수정 시간의 내림차순으로 정렬할것이다.

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")
    # 작성자의 이름과(author.username) 글 작성일을 합친 문자열을 반환한다.

    def get_absolute_url(self):
        return reverse('photo:photo_detail', args=[str(self.id)])  # photo/id
    # 객체의 상세 페이지의 주소를 반환하는 메서드입니다.
    # 객체를 수정했을 때 이동할 주소를 위해 호출되기도 하고 템플릿에서 상세 화면으로 이동하는
    # 링크를 만들 때 호출하기도 합니다. 이런 주소를 만들기 위해서는 reverse 메서드를 사용하는데
    # reverse 메서드는 URL 패턴 이름을 가지고 해당 패턴을 찾아 주소를 만들어주는 함수이다.
