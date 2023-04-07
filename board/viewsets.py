from django.urls import path
from .views import BoardViewSet

# board 목록 조회
board_list = BoardViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

# board detail 조회 + 수정 + 삭제
board_detail = BoardViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns =[
    path('board/', board_list),
    path('board/<int:pk>/', board_detail),
]