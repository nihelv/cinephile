from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'score', 'content',)
    
    title = forms.CharField(
        label='제목',
        label_suffix='',
        widget=forms.TextInput(
            attrs={'class': 'form-control form-field',}
        )
    )

    score = forms.DecimalField(
        label='평점',
        label_suffix='',
        widget=forms.NumberInput(
            attrs={
                'type': 'number',
                'name': 'score',
                'min': '0',
                'max': '5',
                'step': '0.5',
                'class': 'form-control form-field',
            }
        )
    )

    content = forms.CharField(
        label='내용',
        label_suffix='',
        widget=forms.Textarea(
            attrs={'class': 'form-control form-field',}
        )
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)