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

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()  # 기존에 제공했던 기능을 가져와서 context 변수에 저장
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context


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

# category page URL이 왔을 때(FBV로 작업)
def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug) # slug와 동일한 값을 갖는 카테고리를 불러오는 쿼리
        post_list = Post.objects.filter(category=category)

    return render(
        request,
        'blog/post_list.html', # post_list 템플릿을 그대로 사용함
        { # PostList 클래스에서 context로 정의했던 부분을 딕셔너리 형태로 직접 정의해야 함
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'category': category # post_list 템플릿에서 제목 옆에 뱃지를 붙일 때 카테고리 리스트인지 그냥 포스트 리스트인지 판단하는 용으로도 쓰인다.
        }
    )