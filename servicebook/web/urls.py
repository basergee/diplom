from django.urls import path

from .views import (GeneralInfoView, HandbookDetailView, MaintenanceView,
                    ReclamationView)


urlpatterns = [
    path('info/', GeneralInfoView.as_view(), name='info'),
    path('maintenance/', MaintenanceView.as_view(), name='maintenance'),
    path('reclamation/', ReclamationView.as_view(), name='reclamation'),
    path('hb/<int:pk>/', HandbookDetailView.as_view(), name='handbook_detail'),
]
