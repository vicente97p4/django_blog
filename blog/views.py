from django.shortcuts import render
from .models import Post

# Create your views here.


def index(request):
    posts = Post.objects.all().order_by('-pk')

    return render(
        request,
        'blog/index.html',
        {
            'posts': posts,
        }
    )


def single_post_page(request, pk):
    post = Post.objects.get(pk=pk) # pk 필드 값이 pk인 Post 레코드를 가져오라는 의미이다.

    return render(
        request,
        'blog/single_post_page.html',
        {
            'post' : post
        }
    )