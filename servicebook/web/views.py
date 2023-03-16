from django.shortcuts import render
from django.views.generic import ListView, DetailView

from api.models import Vehicle, Handbook, Maintenance, Reclamation


class GeneralInfoView(ListView):
    template_name = 'general-info.html'
    model = Vehicle
    context_object_name = 'vehicle_list'
    # Ограничиваем количество машин на странице
    paginate_by = 10
    # Сортировка по полю 'Дата отгрузки с завода'
    ordering = '-shipping_date'


class MaintenanceView(ListView):
    template_name = 'maintenance.html'
    model = Maintenance
    context_object_name = 'maintenance_list'
    # Ограничиваем количество машин на странице
    paginate_by = 10
    # Сортировка по полю 'Дата проведения ТО'
    ordering = '-maintenance_date'


class ReclamationView(ListView):
    template_name = 'reclamation.html'
    model = Reclamation
    context_object_name = 'reclamation_list'
    # Ограничиваем количество машин на странице
    paginate_by = 10
    # Сортировка по полю 'Дата отказа'
    ordering = '-failure_date'


class HandbookDetailView(DetailView):
    template_name = 'handbook.html'
    model = Handbook
    # context_object_name = 'handbook_detail'

    # def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # context['now'] = timezone.now()
        # return context
