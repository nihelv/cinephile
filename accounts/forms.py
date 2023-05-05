from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

# 사용자 정의 회원 가입 Form
class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control form-field', 'placeholder': '비밀번호'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control form-field', 'placeholder': '비밀번호 확인'}))
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2',)

        widgets = {
            'username': forms.TextInput(
                attrs = {'class': 'form-control form-field', 'placeholder': '아이디',}
            ),
            'email': forms.EmailInput(
                attrs = {'class': 'form-control form-field', 'placeholder': '이메일',}
            ),
            'last_name': forms.TextInput(
                attrs = {'class': 'form-control form-field', 'placeholder': '성',}
            ),
            'first_name': forms.TextInput(
                attrs = {'class': 'form-control form-field', 'placeholder': '이름',}
            ),
        }


# 로그인 Form
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-field',
                'placeholder': '아이디',
            })
    )

    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control form-field',
                'placeholder': '비밀번호',
            })
    )
    

# 사용자 정의 회원 정보 변경 Form
class CustomUserChangeForm(UserChangeForm):
    password = None
    email = forms.EmailField(
        label='이메일',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '이메일',
            }
        )
    )
    first_name = forms.CharField(
        label='이름',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '이름'
            }
        )
    )
    last_name = forms.CharField(
        label='성',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '성'
            }
        )
    )
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name',)