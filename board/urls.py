'''

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.AllBoardView.as_view()),
    # ex: /polls/5/
    path('<int:pk>/', views.OneBoardView.as_view()),
]

'''

from django.urls import path,include
from rest_framework import routers
from .views import BoardViewSet


router = routers.DefaultRouter()
router.register('board', BoardViewSet) #urls.py의 router

urlpatterns = [
    path('', include(router.urls)),
]
