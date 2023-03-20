from django.urls import path

from .views import (GeneralInfoView, HandbookDetailView, MaintenanceView,
                    ReclamationView, login_view, logout_view)


urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('info/', GeneralInfoView.as_view(), name='info'),
    path('maintenance/', MaintenanceView.as_view(), name='maintenance'),
    path('reclamation/', ReclamationView.as_view(), name='reclamation'),
    path('hb/<int:pk>/', HandbookDetailView.as_view(), name='handbook_detail'),
]
