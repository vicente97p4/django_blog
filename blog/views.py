from django.shortcuts import render
from django.views.generic import ListView
from .models import Post

# Create your views here.

# CBV로 작업했을 때


class PostList(ListView):
    model = Post
    ordering = '-pk'

# FBV로 작업했을 때
# def index(request):
#     posts = Post.objects.all().order_by('-pk')
#
#     return render(
#         request,
#         'blog/post_list.html',
#         {
#             'posts': posts,
#         }
#     )


def single_post_page(request, pk):
    post = Post.objects.get(pk=pk) # pk 필드 값이 pk인 Post 레코드를 가져오라는 의미이다.

    return render(
        request,
        'blog/single_post_page.html',
        {
            'post' : post
        }
    )