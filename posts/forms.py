from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content',)
    
    title = forms.CharField(
        label='제목',
        label_suffix='',
        widget=forms.TextInput(
            attrs={'class': 'form-control form-field', 'placeholder': '제목',}
        )
    )

    content = forms.CharField(
        label='내용',
        label_suffix='',
        widget=forms.Textarea(
            attrs={'class': 'form-control form-field', 'placeholder': '내용',}
        )
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)