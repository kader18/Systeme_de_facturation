from . import views
from django.urls import path


urlpatterns = [
    path("", views.HomeView.as_view(), name='home'),
    path("Client/", views.AddCustomerView.as_view(), name='add-customer'),
    path("Facture/", views.AddInvoiceView.as_view(), name='add-invoice'),
    path("vue-facture/<int:pk>", views.InvoiceVisualizationView.as_view(), name='view-invoice'),
    path("facture-pdf/<int:pk>", views.get_invoice_pdf, name='invoice-pdf'),
]

