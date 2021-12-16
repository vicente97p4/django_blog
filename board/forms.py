from django import forms
from .models import Board
from django_summernote.widgets import SummernoteWidget


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'content']
        widgets = {
            'content': SummernoteWidget(),
        }