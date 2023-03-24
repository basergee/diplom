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


# Класс нужен для того, чтобы в формах выводить для клиентов и сервисных
# компаний поле first_name
class UserFirstNameField(forms.ModelChoiceField):
    def label_from_instance(self, user):
        return user.first_name


class VehicleCreateForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'vehicle_model',
            'vehicle_id',
            'engine_model',
            'engine_id',
            'transmission_model',
            'transmission_id',
            'main_axle_model',
            'main_axle_id',
            'driven_axle_model',
            'driven_axle_id',
            'shipping_date',
            'client',
            'consignee',
            'shipping_address',
            'equipment',
            'service_company',
        ]

    def __init__(self, *args, **kwargs):
        # Пользователь нам нужен, но его передача в конструктор базового
        # класса вызовет ошибку, поэтому извлекаем его.
        user = kwargs.pop('user', None)
        super(VehicleCreateForm, self).__init__(*args, **kwargs)

        # Устанавливаем значения для выпадающих списков формы
        self.fields['vehicle_model'].queryset = Handbook.objects.filter(
            handbook_name='VM')
        self.fields['engine_model'].queryset = Handbook.objects.filter(
            handbook_name='EM')
        self.fields['transmission_model'].queryset = Handbook.objects.filter(
            handbook_name='TM')
        self.fields['main_axle_model'].queryset = Handbook.objects.filter(
            handbook_name='MA')
        self.fields['driven_axle_model'].queryset = Handbook.objects.filter(
            handbook_name='DA')
        self.fields['client'] = UserFirstNameField(
            queryset=User.objects.filter(groups__name__in=['Client']))
        self.fields['service_company'] = UserFirstNameField(
            queryset=User.objects.filter(groups__name__in=['ServiceCompany']))


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
        self.fields['service_company'] = UserFirstNameField(
            queryset=User.objects.filter(groups__name__in=['ServiceCompany']))


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
        self.fields['service_company'] = UserFirstNameField(
            queryset=User.objects.filter(groups__name__in=['ServiceCompany']))
