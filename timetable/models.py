from django.db import models
from account.models import School,User,CommonInfo
from datetime import datetime
# Create your models here.

class Lecture(CommonInfo):
    school_id = models.ForeignKey(School, on_delete=models.CASCADE,related_name='lectureId')
    name = models.CharField("강의 이름", max_length=50)
    professor = models.CharField("교수 성함", max_length=20)
    classroom = models.CharField("수업실", max_length=20)
    credit = models.PositiveIntegerField("학수번호")
    time = models.CharField(max_length=255) #요일 및 시간

    def __str__(self):
        return '{} of {} naming {}'.format(self.name, self.professor, self.classroom)

class Timetable(CommonInfo):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mylectureuserId')
    lecture_id = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='mylectureId')
    is_show = models.BooleanField("친구 공개 여부", default=False)

    def __str__(self):
        return '{}'.format(self.user_id.name, self.lecture_id.name)


class Review(CommonInfo):
    timetable_id = models.ForeignKey(Timetable, on_delete=models.CASCADE,related_name='reviewId')
    content = models.CharField("리뷰 내용", max_length=200)

    def __str__(self):
        return '{}'.format(self.content)
