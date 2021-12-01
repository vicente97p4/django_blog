from django.urls import path
from . import views

urlpatterns = [
     path('create_post/', views.PostCreate.as_view()),
     path('tag/<str:slug>/', views.tag_page),
     path('category/<str:slug>/', views.category_page), # 사용자가 category/ 뒤에 문자열이 붙는 URL을 입력하면 그 문자열을 category_page 함수의 매개변수인 slug의 인자로 넘겨준다.
     # path('<int:pk>/', views.single_post_page), # <int:pk>는 정수 형태의 값을 pk라는 변수로 담아 single_post_page로 넘기겠다는 의미이다.
     path('<int:pk>/', views.PostDetail.as_view()),
     # path('', views.index)
     path('', views.PostList.as_view()),
]