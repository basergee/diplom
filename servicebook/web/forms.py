from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from api.models import Maintenance, Handbook, Vehicle, Reclamation


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


class MaintenanceCreateForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = [
            'vehicle',
            'maintenance_type',
            'maintenance_date',
            'operating_time',
            'work_order_id',
            'work_order_date',
            'service_company',
        ]

    def __init__(self, *args, **kwargs):
        # Пользователь нам нужен, но его передача в конструктор базового
        # класса вызовет ошибку, поэтому извлекаем его.
        user = kwargs.pop('user', None)
        super(MaintenanceCreateForm, self).__init__(*args, **kwargs)

        # Устанавливаем значения для выпадающих списков формы
        self.fields['vehicle'].queryset = Vehicle.objects.filter(client=user)
        self.fields['maintenance_type'].queryset = Handbook.objects.filter(
            handbook_name='MT')
        self.fields['service_company'].queryset = User.objects.filter(
            groups__name__in=['ServiceCompany'])


class ReclamationCreateForm(forms.ModelForm):
    class Meta:
        model = Reclamation
        fields = [
            'vehicle',
            'failure_date',
            'operating_time',
            'failure_node',
            'failure_description',
            'repair_description',
            'spare_parts',
            'repair_date',
            'service_company',
        ]

    def __init__(self, *args, **kwargs):
        # Пользователь нам нужен, но его передача в конструктор базового
        # класса вызовет ошибку, поэтому извлекаем его.
        user = kwargs.pop('user', None)
        super(ReclamationCreateForm, self).__init__(*args, **kwargs)

        # Устанавливаем значения для выпадающих списков формы
        self.fields['vehicle'].queryset = Vehicle.objects.filter(client=user)
        self.fields['failure_node'].queryset = Handbook.objects.filter(
            handbook_name='FN')
        self.fields['repair_description'].queryset = Handbook.objects.filter(
            handbook_name='RD')
        self.fields['service_company'].queryset = User.objects.filter(
            groups__name__in=['ServiceCompany'])
