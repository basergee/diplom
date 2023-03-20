from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate

from api.models import Vehicle, Handbook, Maintenance, Reclamation
from .forms import UserLoginForm


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


class GeneralInfoView(ListView):
    template_name = 'general-info.html'
    model = Vehicle
    context_object_name = 'vehicle_list'
    # Ограничиваем количество машин на странице
    paginate_by = 10
    # Сортировка по полю 'Дата отгрузки с завода'
    ordering = '-shipping_date'

    def get(self, request, *args, **kwargs):
        vm = request.GET.get('vehicle')
        em = request.GET.get('engine')
        tm = request.GET.get('transmission')
        mam = request.GET.get('mainaxle')
        dam = request.GET.get('drivenaxle')

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

        if not res:
            # Если запросов нет, выводим все объекты
            qs = Vehicle.objects.all()
        else:
            # Объединяем все запросы в один и фильтруем сразу по всем
            # переданным параметрам
            q = res[0]
            for i in range(1, len(res)):
                q = q & res[i]

            qs = Vehicle.objects.filter(q)

        context = {
            self.context_object_name: qs
        }
        return render(request, self.template_name, context)


class MaintenanceView(ListView):
    template_name = 'maintenance.html'
    model = Maintenance
    context_object_name = 'maintenance_list'
    # Ограничиваем количество машин на странице
    paginate_by = 10
    # Сортировка по полю 'Дата проведения ТО'
    ordering = '-maintenance_date'

    def get(self, request, *args, **kwargs):
        # вид ТО
        mt = request.GET.get('mtype')
        # зав.номер машины
        vid = request.GET.get('vehicle')
        # сервисная компания
        sc = request.GET.get('service')

        # Из полученных параметров подготавливаем объекты запросов
        res = []
        if mt != '' and mt is not None:
            res.append(Q(maintenance_type__title__icontains=mt))
        if vid != '' and vid is not None:
            res.append(Q(vehicle__vehicle_id__icontains=vid))
        if sc != '' and sc is not None:
            res.append(Q(service_company__title__icontains=sc))

        if not res:
            # Если запросов нет, выводим все объекты
            qs = Maintenance.objects.all()
        else:
            # Объединяем все запросы в один и фильтруем сразу по всем
            # переданным параметрам
            q = res[0]
            for i in range(1, len(res)):
                q = q & res[i]

            qs = Maintenance.objects.filter(q)

        context = {
            self.context_object_name: qs
        }
        return render(request, self.template_name, context)


class ReclamationView(ListView):
    template_name = 'reclamation.html'
    model = Reclamation
    context_object_name = 'reclamation_list'
    # Ограничиваем количество машин на странице
    paginate_by = 10
    # Сортировка по полю 'Дата отказа'
    ordering = '-failure_date'

    def get(self, request, *args, **kwargs):
        # узел отказа
        fn = request.GET.get('fnode')
        # способ восстановления
        rd = request.GET.get('repairdescription')
        # сервисная компания
        sc = request.GET.get('service')

        # Из полученных параметров подготавливаем объекты запросов
        res = []
        if fn != '' and fn is not None:
            res.append(Q(failure_node__title__icontains=fn))
        if rd != '' and rd is not None:
            res.append(Q(repair_description__title__icontains=rd))
        if sc != '' and sc is not None:
            res.append(Q(service_company__title__icontains=sc))

        if not res:
            # Если запросов нет, выводим все объекты
            qs = Reclamation.objects.all()
        else:
            # Объединяем все запросы в один и фильтруем сразу по всем
            # переданным параметрам
            q = res[0]
            for i in range(1, len(res)):
                q = q & res[i]

            qs = Reclamation.objects.filter(q)

        context = {
            self.context_object_name: qs
        }
        return render(request, self.template_name, context)


class HandbookDetailView(DetailView):
    template_name = 'handbook.html'
    model = Handbook
    # context_object_name = 'handbook_detail'

    # def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # context['now'] = timezone.now()
        # return context
