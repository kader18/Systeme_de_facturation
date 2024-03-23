from . import views
from django.urls import path


urlpatterns = [
    path("", views.HomeView.as_view(), name='home'),
    path("Client/", views.AddCustomerView.as_view(), name='add-customer'),
    path("Facture/", views.AddInvoiceView.as_view(), name='add-invoice'),
]

