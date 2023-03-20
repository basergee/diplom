from django import forms
from django.contrib.auth import authenticate


class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'id': "floatingInput"
            }
        ),
        label='Логин',
        label_suffix=''
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
                'id': "floatingPassword"
            }
        ),
        label='Пароль',
        label_suffix=''
    )

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Пользователь не существует')
            if not user.check_password(password):
                raise forms.ValidationError('Неправильный пароль')
            if not user.is_active:
                raise forms.ValidationError('Пользователь не активен')
        return super(UserLoginForm, self).clean(*args, **kwargs)
