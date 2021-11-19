from django.urls import path
from . import views

urlpatterns = [
     # path('<int:pk>/', views.single_post_page), # <int:pk>는 정수 형태의 값을 pk라는 변수로 담아 single_post_page로 넘기겠다는 의미이다.
     path('<int:pk>/', views.PostDetail.as_view()),
     # path('', views.index)
     path('', views.PostList.as_view()),
]