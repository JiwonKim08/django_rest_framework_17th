from rest_framework import serializers
from .models import *
from account.serializers import SchoolSerializer,UserSerializer
from board.serializers import BoardSerializer

class LectureSerializer(serializers.ModelSerializer):
    school_id = SchoolSerializer

    class Meta:
        model = Lecture
        fields = '__all__'


class TimetableSerializer(serializers.ModelSerializer):
    user_id = UserSerializer
    lecture_id =LectureSerializer
    class Meta:
        model = Timetable
        fields = '__all__'
class Review(serializers.ModelSerializer):
    timetable_id = TimetableSerializer

    class Meta:
        model = Review
        fields = '__all__'