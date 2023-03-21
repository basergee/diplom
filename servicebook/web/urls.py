from django.urls import path

from .views import (GeneralInfoView, HandbookDetailView, MaintenanceView,
                    ReclamationView, login_view, logout_view, IndexView,
                    VehicleCreateView, HandbookUpdateView,
                    ReclamationCreateView, ReclamationUpdateView,
                    MaintenanceCreateView, MaintenanceUpdateView,
                    VehicleUpdateView, HandbookCreateView)


urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('info/', GeneralInfoView.as_view(), name='info'),

    path('vehicle/add/', VehicleCreateView.as_view(), name='vehicle_add'),
    path('vehicle/edit/<int:pk>/', VehicleUpdateView.as_view(), name='vehicle_edit'),

    path('maintenance/', MaintenanceView.as_view(), name='maintenance'),
    path('maintenance/add', MaintenanceCreateView.as_view(), name='maintenance_add'),
    path('maintenance/edit/<int:pk>/', MaintenanceUpdateView.as_view(), name='maintenance_edit'),

    path('reclamation/', ReclamationView.as_view(), name='reclamation'),
    path('reclamation/add/', ReclamationCreateView.as_view(), name='reclamation_add'),
    path('reclamation/edit/<int:pk>/', ReclamationUpdateView.as_view(), name='reclamation_edit'),

    path('hb/<int:pk>/', HandbookDetailView.as_view(), name='handbook_detail'),
    path('hb/add/', HandbookCreateView.as_view(), name='handbook_add'),
    path('hb/edit/<int:pk>/', HandbookUpdateView.as_view(), name='handbook_edit'),
]
