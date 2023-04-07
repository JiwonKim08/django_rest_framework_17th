'''
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *

class AllBoardView(APIView):
    def get(self,request,format=None): #모든 게시판
        try:
            boardlists = Board.objects.all()
            serializer = BoardSerializer(boardlists, many=True)
            #리스트로 반환하는 boardlists
            return Response(serializer.data)
        except AttributeError as e:
            print(e)
            return Response("message: error")

    def post(self, request,format=None):
        data = request.data
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

class OneBoardView(APIView):
    def get(self, request, pk): #원하는 게시판 가져오기
        try:
            board = Board.objects.get(id=pk)
            serializer = BoardSerializer(board)
            return Response(serializer.data, status=201)
        except ObjectDoesNotExist as e:
            print(e)
            return Response({"message: error"})

    def delete(self, request, pk):
        #soft delete #post(deleted_at 넣어주면 되니까?)
        try:
            board = Board.objects.get(id=pk)
            board.delete()
            return Response(status=200)
        except ObjectDoesNotExist as e:
            print(e)
            return Response({"message: not exist"})
'''


#filter
from rest_framework import viewsets

from .serializers import *
from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend

class BoardFilter(FilterSet):
    #필터 걸 속성
    #school_id = filters.NumberFilter(field_name='school_id_id')
    name = filters.CharFilter(field_name='name')

    def filter_school_id(self, queryset): #필터 메서드로 구현
        filtered_queryset = filters.NumberFilter(field_name='school_id_id')
        return filtered_queryset


    class Meta:
        model = Board #사용할 모델
        fields = ['name','school_id'] #사용할 속성


#ModelViewSet을 상속함으로써 crud 기능이 5줄로 끝남
class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    queryset = Board.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = BoardFilter









