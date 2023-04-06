from rest_framework import serializers
from .models import *
from account.serializers import SchoolSerializer,UserSerializer

class BoardSerializer(serializers.ModelSerializer):
    school_id = SchoolSerializer

    class Meta:
        model = Board
        fields = '__all__'

class FixedboardSerializer(serializers.ModelSerializer):
    board_id = BoardSerializer
    user_id = UserSerializer

    class Meta:
        model = Fixed_board
        fields = '__all__'
class PostSerializer(serializers.ModelSerializer):
    board_id = BoardSerializer
    class Meta:
        model = Post
        fields = '__all__'
class ScrapSerializer(serializers.ModelSerializer):
    user_id = UserSerializer
    post_id = PostSerializer

    class Meta:
        model = Scrap
        fields = '__all__'


class PhotoSerializer(serializers.ModelSerializer):
    post_id = PostSerializer

    class Meta:
        model = Photo
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    user_id = UserSerializer
    post_id = PostSerializer
    #댓글 자기 참조 안 넣음
    class Meta:
        model = Comment
        fields = '__all__'