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

