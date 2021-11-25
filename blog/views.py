from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category

# Create your views here.

# CBV로 작업했을 때


class PostList(ListView):
    model = Post
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data() # 기존에 제공했던 기능을 가져와서 context 변수에 저장
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

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


class PostDetail(DetailView):
    model = Post


# FBV로 작업했을 때
# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk) # pk 필드 값이 pk인 Post 레코드를 가져오라는 의미이다.
#
#     return render(
#         request,
#         'blog/post_detail.html',
#         {
#             'post' : post
#         }
#     )