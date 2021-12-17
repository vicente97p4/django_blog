from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Board(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    board_good = models.ManyToManyField(User, related_name='board_good', blank=True)

    def __str__(self):
        return f'[{self.pk}] {self.title}::{self.author}'

    def get_absolute_url(self):
        return f'/board/{self.pk}/'


class BoardComment(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.board.get_absolute_url()}#comment-{self.pk}'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://picsum.photos/seed/{self.author.pk}/60/60'