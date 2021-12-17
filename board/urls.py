from django.urls import path
from . import views

urlpatterns = [
     path('good/', views.good, name='board_good'),
     path('<int:pk>/new_comment/', views.new_boardcomment),
     path('search/<str:q>/', views.BoardSearch.as_view()),
     path('create/', views.BoardCreate.as_view()),
     path('<int:pk>/', views.BoardDetail.as_view()),
     path('', views.BoardList.as_view()),
]
