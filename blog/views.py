from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from .models import Post, Category, Tag, Comment
from .forms import CommentForm
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from datetime import date, datetime, timedelta
import json
# Create your views here.

# CBV로 작업했을 때


class PostList(ListView):
    model = Post
    ordering = '-pk'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data() # 기존에 제공했던 기능을 가져와서 context 변수에 저장
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        lst = context['post_list']

        temp = []
        for i in range(0, len(lst), 2):
            tmp = []
            tmp.append(lst[i])
            if i+1 < len(lst):
                tmp.append(lst[i+1])
            temp.append(tmp)
        context['post_list'] = temp
        page = context['page_obj']
        lst = page.paginator.page_range
        if page.paginator.num_pages > 10:
            if page.number <= 5:
                lst = list(range(1, 11))
            elif page.paginator.num_pages-5 <= page.number <= page.paginator.num_pages:
                lst = list(range(page.paginator.num_pages-9, page.paginator.num_pages+1))
            else:
                lst = list(range(page.paginator.num_pages-4, page.paginator.num_pages+6))
        context['page_range'] = lst

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


# class PostDetail(DetailView):
#     model = Post
#
#     def get_context_data(self, **kwargs):
#         context = super(PostDetail, self).get_context_data()  # 기존에 제공했던 기능을 가져와서 context 변수에 저장
#         context['categories'] = Category.objects.all()
#         context['no_category_post_count'] = Post.objects.filter(category=None).count()
#         context['comment_form'] = CommentForm
#         return context


def post_detail(request, pk):
    login_session = request.session.get('login_session', '')
    context = {'login_session': login_session}

    post = get_object_or_404(Post, id=pk)
    context['post'] = post
    context['categories'] = Category.objects.all()
    context['no_category_post_count'] = Post.objects.filter(category=None).count()
    context['comment_form'] = CommentForm

    # 글쓴이인지 확인
    if post.author.id == login_session:
        context['writer'] = True
    else:
        context['writer'] = False

    response = render(
        request,
        'blog/post_detail.html',
        context
    )

    cookie_value = request.COOKIES.get('enter_post', '_')

    if f'{pk}' not in cookie_value:
        cookie_value += f'{pk}_'
        response.set_cookie('enter_post', value=cookie_value, httponly=True)
        post.view_cnt += 1
        post.save()

    return response


class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_superuser or current_user.is_staff):
            form.instance.author = current_user
            response = super(PostCreate, self).form_valid(form)

            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()

                tags_str = tags_str.replace(',', ';')
                tags_str = tags_str.replace('#', ';')
                tags_list = tags_str.split(';')

                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag) # 새로 저장된 포스트는 self.object로 가져올 수 있게 장고가 구성한다.

            return response
        else:
            return redirect('/blog/')


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    template_name = 'blog/post_update_form.html'

    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = []
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tags_str_default'] = '; '.join(tags_str_list)

        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()

        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()

            tags_str = tags_str.replace(',', ';')
            tags_str = tags_str.replace('#', ';')
            tags_list = tags_str.split(';')

            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)

            return response
        else:
            return redirect('/blog/')


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

    temp = []
    for i in range(0, len(post_list), 2):
        tmp = []
        tmp.append(post_list[i])
        if i + 1 < len(post_list):
            tmp.append(post_list[i + 1])
        temp.append(tmp)
    post_list = temp
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


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'tag': tag,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count()
        }
    )


def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST': # 만일 그냥 url에 /new_comment를 입력하여 접속하면 get method를 사용하여 접속하게 된다. 그럴 경우 redirect 시켜준다.
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False) # 저장하는 기능 잠시 멈춤
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())

    else:
        raise PermissionDenied


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied


class PostSearch(PostList):
    paginate_by = 10

    def get_queryset(self):
        q = self.kwargs['q']
        post_list = Post.objects.filter(
            Q(title__contains=q) | Q(tags__name__contains=q)
        ).distinct().order_by('-pk')

        return post_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'

        return context


def good(request):
    if request.is_ajax():

        pk = request.GET['pk']
        post = Post.objects.get(pk=pk)

        if not request.user.is_authenticated:
            print('operated')
            message = '로그인이 필요합니다.'
            context = {'good_count': post.good.count(), 'message': message}
            return HttpResponse(json.dumps(context), content_type='application/json')

        user = request.user
        if post.good.filter(id=user.id):
            post.good.remove(user)
            message = '좋아요 취소'
        else:
            post.good.add(user)
            message = '좋아요'
        context = {'good_count': post.good.count(), 'message': message}
        return HttpResponse(json.dumps(context), content_type='application/json')

