from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School #사용할 모델
        fields = '__all__' #사용할 모델의 필드
class UserSerializer(serializers.ModelSerializer):
    school_id = SchoolSerializer
    class Meta:
        model=User 
        fields = '__all__'


class FriendSerializer(serializers.ModelSerializer):
    follower_id = UserSerializer
    followee_id = UserSerializer

    class Meta:
        model = Freind
        field = ['follower_id','followee_id']
