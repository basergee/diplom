from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from api.models import Vehicle, Handbook, Maintenance, Reclamation
from .forms import UserLoginForm, MaintenanceCreateForm


def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('info')

    context = {
        'form': form
    }
    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect('index')


class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'search_results'
    model = Vehicle

    def get(self, request, *args, **kwargs):
        vehicle_id = request.GET.get('vehicleid')

        if vehicle_id != '' and vehicle_id is not None:
            qs = Vehicle.objects.filter(vehicle_id__icontains=vehicle_id)
        else:
            # Если запросов нет, ничего не выводим
            qs = []

        context = {
            self.context_object_name: qs
        }
        return render(request, self.template_name, context)


class VehiclesView(LoginRequiredMixin, ListView):
    template_name = 'vehicle.html'
    model = Vehicle
    context_object_name = 'vehicle_list'

    login_url = reverse_lazy('login')

    # Ограничиваем количество машин на странице
    paginate_by = 10
    # Сортировка по полю 'Дата отгрузки с завода'
    ordering = '-shipping_date'

    def get_queryset(self):
        vm = self.request.GET.get('vehicle')
        em = self.request.GET.get('engine')
        tm = self.request.GET.get('transmission')
        mam = self.request.GET.get('mainaxle')
        dam = self.request.GET.get('drivenaxle')

        # Из полученных параметров подготавливаем объекты запросов
        res = []
        if vm != '' and vm is not None:
            res.append(Q(vehicle_model__title__icontains=vm))
        if em != '' and em is not None:
            res.append(Q(engine_model__title__icontains=em))
        if tm != '' and tm is not None:
            res.append(Q(transmission_model__title__icontains=tm))
        if mam != '' and mam is not None:
            res.append(Q(main_axle_model__title__icontains=mam))
        if dam != '' and dam is not None:
            res.append(Q(driven_axle_model__title__icontains=dam))

        qs = None  # Объекты, которые будут выведены на страницу

        if self.request.user.groups.filter(name='Client').exists():
            # Клиент видит только свои машины
            qs = Vehicle.objects.filter(client=self.request.user)
        elif self.request.user.groups.filter(name='ServiceCompany').exists():
            # Сервисная компания видит только машины, которые обслуживает
            qs = Vehicle.objects.filter(service_company=self.request.user)
        elif self.request.user.groups.filter(name='Manager').exists():
            # Менеджер видит все машины
            qs = Vehicle.objects.all()
        else:
            # Пользователь не состоит в группе. Это ошибка!
            # Стоит как-то уведомить об этом: может кинуть исключение
            qs = Vehicle.objects.none()

        if res:
            # Объединяем все запросы в один и фильтруем сразу по всем
            # переданным параметрам
            q = res[0]
            for i in range(1, len(res)):
                q = q & res[i]

            qs = Vehicle.objects.filter(q)

        return qs


class VehicleCreateView(LoginRequiredMixin, CreateView):
    template_name = 'add_or_edit_object_form.html'
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
    login_url = reverse_lazy('login')


class VehicleUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'add_or_edit_object_form.html'
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
    login_url = reverse_lazy('login')


class MaintenanceView(LoginRequiredMixin, ListView):
    template_name = 'maintenance.html'
    model = Maintenance
    context_object_name = 'maintenance_list'

    login_url = reverse_lazy('login')

    # Ограничиваем количество машин на странице
    paginate_by = 10
    # Сортировка по полю 'Дата проведения ТО'
    ordering = '-maintenance_date'

    def get_queryset(self):
        # вид ТО
        mt = self.request.GET.get('mtype')
        # зав.номер машины
        vid = self.request.GET.get('vehicle')
        # сервисная компания
        sc = self.request.GET.get('service')

        # Из полученных параметров подготавливаем объекты запросов
        res = []
        if mt != '' and mt is not None:
            res.append(Q(maintenance_type__title__icontains=mt))
        if vid != '' and vid is not None:
            res.append(Q(vehicle__vehicle_id__icontains=vid))
        if sc != '' and sc is not None:
            res.append(Q(service_company__title__icontains=sc))

        qs = None  # Объекты, которые будут выведены на страницу

        if self.request.user.groups.filter(name='Client').exists():
            # Клиент видит только свои машины
            qs = Maintenance.objects.filter(vehicle__client=self.request.user)
        elif self.request.user.groups.filter(name='ServiceCompany').exists():
            # Сервисная компания видит только машины, которые обслуживает
            qs = Maintenance.objects.filter(vehicle__service_company=self.request.user)
        elif self.request.user.groups.filter(name='Manager').exists():
            # Менеджер видит все машины
            qs = Maintenance.objects.all()
        else:
            # Пользователь не состоит в группе. Это ошибка!
            # Стоит как-то уведомить об этом: может кинуть исключение
            qs = Maintenance.objects.none()

        if res:
            # Объединяем все запросы в один и фильтруем сразу по всем
            # переданным параметрам
            q = res[0]
            for i in range(1, len(res)):
                q = q & res[i]

            qs = Maintenance.objects.filter(q)

        return qs


class MaintenanceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'add_or_edit_object_form.html'
    model = Maintenance
    # fields = [
    #     'vehicle',
    #     'maintenance_type',
    #     'maintenance_date',
    #     'operating_time',
    #     'work_order_id',
    #     'work_order_date',
    #     'service_company',
    # ]
    login_url = reverse_lazy('login')
    form_class = MaintenanceCreateForm
    success_url = reverse_lazy('maintenance')

    def get_form_kwargs(self):
        kwargs = super(MaintenanceCreateView, self).get_form_kwargs()
        # Добавляем текущего пользователя к форме, чтобы можно было
        # отфильтровать поля в форме
        kwargs.update({'user': self.request.user})
        return kwargs

    def test_func(self):
        print('----->')
        return any([
            self.request.user.groups.filter(name='Client').exists(),
            self.request.user.groups.filter(name='Service').exists(),
            self.request.user.groups.filter(name='Manager').exists()
        ])


class MaintenanceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'add_or_edit_object_form.html'
    model = Maintenance
    # fields = [
    #     'vehicle',
    #     'maintenance_type',
    #     'maintenance_date',
    #     'operating_time',
    #     'work_order_id',
    #     'work_order_date',
    #     'service_company',
    # ]
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('maintenance')
    form_class = MaintenanceCreateForm

    def get_form_kwargs(self):
        kwargs = super(MaintenanceUpdateView, self).get_form_kwargs()
        # Добавляем текущего пользователя к форме, чтобы можно было
        # отфильтровать поля в форме
        kwargs.update({'user': self.request.user})
        return kwargs

    def test_func(self):
        user = self.request.user

        if user.groups.filter(name='Manager').exists():
            # Менеджер может редактировать любой объект
            return True

        # Узнаем ключ объекта, который пытаемся редактировать
        maintenance_id = int(self.request.path.split('/')[-2])

        # Чтобы иметь доступ, пользователь должен быть клиентом, владеющим
        # машиной, или сервисной компанией, обслуживающей машину
        if user.groups.filter(name='Client').exists():
            # Пользователь -- клиент. Проверим, что машина, запись о ТО которой
            # хочет получить пользователь, принадлежит ему
            return Maintenance.objects.get(pk=maintenance_id).vehicle.client == user

        if user.groups.filter(name='ServiceCompany').exists():
            # Пользователь -- сервисная компания. Проверим, что машина, запись
            # о ТО которой хочет получить пользователь, обслуживается
            # этой сервисной компанией
            return Maintenance.objects.get(pk=maintenance_id).service_company == user

        return False


class ReclamationView(LoginRequiredMixin, ListView):
    template_name = 'reclamation.html'
    model = Reclamation
    context_object_name = 'reclamation_list'

    login_url = reverse_lazy('login')

    # Ограничиваем количество машин на странице
    paginate_by = 10
    # Сортировка по полю 'Дата отказа'
    ordering = '-failure_date'

    def get_queryset(self):
        # узел отказа
        fn = self.request.GET.get('fnode')
        # способ восстановления
        rd = self.request.GET.get('repairdescription')
        # сервисная компания
        sc = self.request.GET.get('service')

        # Из полученных параметров подготавливаем объекты запросов
        res = []
        if fn != '' and fn is not None:
            res.append(Q(failure_node__title__icontains=fn))
        if rd != '' and rd is not None:
            res.append(Q(repair_description__title__icontains=rd))
        if sc != '' and sc is not None:
            res.append(Q(service_company__title__icontains=sc))

        qs = None  # Объекты, которые будут выведены на страницу

        if self.request.user.groups.filter(name='Client').exists():
            # Клиент видит только свои машины
            qs = Reclamation.objects.filter(vehicle__client=self.request.user)
        elif self.request.user.groups.filter(name='ServiceCompany').exists():
            # Сервисная компания видит только машины, которые обслуживает
            qs = Reclamation.objects.filter(
                vehicle__service_company=self.request.user)
        elif self.request.user.groups.filter(name='Manager').exists():
            # Менеджер видит все машины
            qs = Reclamation.objects.all()
        else:
            # Пользователь не состоит в группе. Это ошибка!
            # Стоит как-то уведомить об этом: может кинуть исключение
            qs = Reclamation.objects.none()

        if res:
            # Объединяем все запросы в один и фильтруем сразу по всем
            # переданным параметрам
            q = res[0]
            for i in range(1, len(res)):
                q = q & res[i]

            qs = Reclamation.objects.filter(q)

        return qs


class ReclamationCreateView(LoginRequiredMixin, CreateView):
    template_name = 'add_or_edit_object_form.html'
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
        'downtime',
    ]
    login_url = reverse_lazy('login')


class ReclamationUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'add_or_edit_object_form.html'
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
        'downtime',
    ]
    login_url = reverse_lazy('login')


class HandbookDetailView(DetailView):
    template_name = 'handbook.html'
    model = Handbook
    # context_object_name = 'handbook_detail'

    # def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # context['now'] = timezone.now()
        # return context


class HandbookCreateView(LoginRequiredMixin, CreateView):
    template_name = 'add_or_edit_object_form.html'
    model = Handbook
    fields = [
        'handbook_name',
        'title',
        'description'
    ]
    login_url = reverse_lazy('login')


class HandbookUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'add_or_edit_object_form.html'
    model = Handbook
    fields = [
        'handbook_name',
        'title',
        'description'
    ]
    login_url = reverse_lazy('login')
