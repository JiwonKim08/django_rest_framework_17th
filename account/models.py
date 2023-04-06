
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager  # 임포트
from datetime import datetime

class CommonInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True) #생성 시간
    updated_at = models.DateTimeField(auto_now=True) #수정 시간
    deleted_at = models.DateTimeField(null=True) #삭제 시간


     #현수님 코드를 보며 댓글-대댓글 삭제여부에 대한 고민을 하게되었다.

    #상속 허용
    class Meta:
        abstract = True

    #DB에 저장된 내용은 가능하면 지우지 않는 게 좋음.
    #따라서 is_deleted로 사용자한테 지우는 척만하고, DB에는 deleted_at
    #으로 삭제요청시간을 기록함. 실제로는 정보를 지우지 않음.
    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = datetime.now()
        self.save()

class School(CommonInfo):
    #기본키 자동생성
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    # 필수로 필요한 데이터를 선언
    def create_user(self, username, password):
        if not username:
            raise ValueError('Users must have an username')
        if not password:
            raise ValueError('Password must have and password')

        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # python manage.py createsuperuser 사용 시 해당 함수가 사용됨
    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            email,
            username=username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    # DB에 저장할 데이터를 선언
    school_id = models.ForeignKey(School, on_delete=models.CASCADE, related_name='schoolId') # 외래키 자동생성
    user_id = models.CharField("사용자 계정", max_length=20, unique=True)
    email = models.EmailField("이메일", max_length=255, unique=True)
    profile_image = models.URLField(default="")  # url 형태로 저장하는게 더 좋음
    nickname = models.CharField("닉네임", max_length=20, unique=True)
    fullname = models.CharField("이름", max_length=20)
    studentNo = models.PositiveIntegerField("학번",default=21)

    # 활성화 여부 (기본값은 True) => 필수 설정
    is_active = models.BooleanField(default=True)

    # 관리자 권한 여부 (기본값은 False) => 필수 설정 : role의 역할
    is_admin = models.BooleanField(default=False)

    # 어드민 계정을 만들 때 입력받을 정보 ex) email
    # 사용하지 않더라도 선언이 되어야함
    # USERNAME_FIELD와 비밀번호는 기본적으로 포함되어있음

    REQUIRED_FIELDS = ['username'] #필수로 값을 받아야하는 필드
    USERNAME_FIELD = 'username'

    # custom user 생성 시 필요
    objects = UserManager()

    #class Meta:
    #   db_table = ""

    # 어드민 페이지에서 데이터에 제목을 어떻게 붙여줄 것인지 지정
    def __str__(self):
        return f"{self.username} / {self.email} 님의 계정입니다"


class Freind(CommonInfo):
    follower_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followerId',primary_key=True)
    followee_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followeeId')

    def __str__(self):
        return '{} and {} became friends '.format(self.follower_id, self.followee_id)
