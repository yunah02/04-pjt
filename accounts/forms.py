from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)


class BootstrapFormMixin:
    """모든 입력 칸에 Bootstrap 클래스를 붙여 주는 믹스인"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = 'form-select' if isinstance(field.widget, forms.Select) else 'form-control'
            field.widget.attrs['class'] = css


class CustomAuthenticationForm(BootstrapFormMixin, AuthenticationForm):
    """로그인 폼"""


class CustomUserCreationForm(BootstrapFormMixin, UserCreationForm):
    """회원가입 폼 : 부모 Meta.model 을 우리 User 로 교체"""

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username',)


class CustomUserChangeForm(BootstrapFormMixin, UserChangeForm):
    """회원정보수정 폼 : 비밀번호·권한 칸은 노출하지 않음"""

    password = None

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name')


class CustomPasswordChangeForm(BootstrapFormMixin, PasswordChangeForm):
    """비밀번호 변경 폼"""