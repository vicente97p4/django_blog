from django.shortcuts import render
from blog.models import Post
# Create your views here.


def landing(request):
    recent_posts = Post.objects.order_by('-pk')[:3]
    hot_posts = Post.objects.all()
    hot_posts = sorted(hot_posts, key=lambda x: x.good.count(), reverse=True)[:3]

    many_view_posts = Post.objects.order_by()[:3]
    return render(
        request,
        'single_pages/landing.html',
        {
            'recent_posts' : recent_posts,
            'hot_posts': hot_posts,
            'many_view_posts': many_view_posts
        }
    )

def about_me(request):
    return render(
        request,
        'single_pages/about_me.html'
    )