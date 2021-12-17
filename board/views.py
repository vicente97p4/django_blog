from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .forms import CommentForm
from .models import Board
from .forms import BoardForm
from django.db.models import Q
from django.http import HttpResponse
import json

# Create your views here.
class BoardList(ListView):
    model = Board
    paginate_by = 10
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BoardList, self).get_context_data()  # 기존에 제공했던 기능을 가져와서 context 변수에 저장
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

class BoardDetail(DetailView):
    model = Board

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BoardDetail, self).get_context_data()  # 기존에 제공했던 기능을 가져와서 context 변수에 저장
        context['comment_form'] = CommentForm

        return context


class BoardCreate(LoginRequiredMixin, CreateView):
    model = Board
    form_class = BoardForm

    def form_valid(self, form):
        current_user = self.request.user

        if current_user.is_authenticated:
            form.instance.author = current_user
            response = super(BoardCreate, self).form_valid(form)

            return response
        else:
            redirect('/board/')


class BoardSearch(BoardList):
    paginate_by = 10

    def get_queryset(self):
        q = self.kwargs['q']
        board_list = Board.objects.filter(
            Q(title__contains=q) | Q(author__username__contains=q) | Q(pk__contains=q)
        ).distinct().order_by('-pk')

        return board_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BoardSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'검색: {q} ({self.get_queryset().count()})'

        return context


def new_boardcomment(request, pk):
    if request.user.is_authenticated:
        board = get_object_or_404(Board, pk=pk)

        if request.method == 'POST': # 만일 그냥 url에 /new_comment를 입력하여 접속하면 get method를 사용하여 접속하게 된다. 그럴 경우 redirect 시켜준다.
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False) # 저장하는 기능 잠시 멈춤
                comment.board = board
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(board.get_absolute_url())
    else:
        raise PermissionDenied


def good(request):
    if request.is_ajax():
        pk = request.GET['pk']
        board = Board.objects.get(pk=pk)

        if not request.user.is_authenticated:
            message = '로그인이 필요합니다.'
            context = {'good_count': board.board_good.count(), 'message': message}
            return HttpResponse(json.dumps(context), content_type='application/json')

        user = request.user
        if board.board_good.filter(id=user.id):
            board.board_good.remove(user)
            message = '좋아요 취소'
        else:
            board.board_good.add(user)
            message = '좋아요'
        context = {'good_count': board.board_good.count(), 'message': message}
        return HttpResponse(json.dumps(context), content_type='application/json')