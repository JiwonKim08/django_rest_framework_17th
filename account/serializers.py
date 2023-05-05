from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School #사용할 모델
        fields = '__all__' #사용할 모델의 필드

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }


class SignUpSerializer(serializers.ModelSerializer):

    #추가옵션

    user_id = serializers.CharField(
        required=True,
        write_only=True,
        max_length=30
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    email = serializers.CharField(
        required=True,
        write_only=True,
        max_length=255
    )

    nickname = serializers.CharField(
        required=True,
        write_only=True,
        max_length=255
    )



    class Meta:
        model = User
        fields = ('user_id','email','password','nickname')

    # def validate(self, data):
    #     user_id = data.get('user_id', None)
    #
    #     # 이미 존재하는 계정인지 확인
    #     if User.objects.filter(user_id=user_id).exists():
    #         raise serializers.ValidationError("User already exists")
    #     return data


    #데이터베이스에 저장
    def save(self, request):
      print("1")
      user = User.objects.create_user(
          email=self.validated_data['email'],
          user_id=self.validated_data['user_id'],
          password=self.validated_data['password'],
          nickname=self.validated_data['nickname']
      )
      user.save()
      return user



class LoginSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(
        required=True,
        write_only=True,
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['user_id', 'password']


    #아이디랑 비밀번호가 맞는지 확인
    def validate(self, data):
        user_id = data.get('user_id', None)
        password = data.get('password', None)

        if User.objects.filter(user_id=user_id).exists():
            user = User.objects.get(user_id=user_id)

            if not user.check_password(password):
                raise serializers.ValidationError("wrong password")
        else:
            raise serializers.ValidationError("user account not exist")

        #유저가 존재하고, 아이디와 비밀번호가 일치한다면 RefreshToken.for_user를 이용해
        #user객체로부터 refresh token과 access token 생성
        token = RefreshToken.for_user(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        data = {
            'user_id':user_id,
            'user': user,
            'access_token': access_token,
            'refresh_token': refresh_token,
        }

        return data
