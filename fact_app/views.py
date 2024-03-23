from django.shortcuts import render
from django.views import View
from .models import *
from django.contrib import messages



class HomeView(View):
    """Vue principale"""

    templates_name = 'index.html'
    invoices = Invoice.objects.select_related('customer', 'save_by').all()

    context = {
        'invoices': invoices,
    }

    def get(self, request, *args, **kwargs):
        return render(request, self.templates_name, self.context)
    

    def post(self, request, *args, **kwargs):
        return render(request, self.templates_name, self.context)
    
class AddCustomerView(View):

    """Ajout d'un nouveau client"""
    
    templates_name = 'add_customer.html'

    customers = Customer.objects.select_related('save_by').all()

    context = {
        'customers':customers,
    }

    def get(self, request, *args, **kwargs):
        return render(request, self.templates_name, self.context)
    

    def post(self, request, *args, **kwargs):
        data = request.POST
        
        context = {
            "name": data.get('name'),
            "email": data.get('email'),
            "phone": data.get('phone'),
            "address": data.get('address'),
            "sex": data.get('sex'),
            "age": data.get('age'),
            "city": data.get('city'),
            "zip_code": data.get('zip'),
            "save_by": request.user

        }

        try:
            created = Customer.objects.create(**context)
            if created:
                messages.success(request,f"Le client {data.get('name')} a été créé avec succès")
            else:
                 messages.error(request, "Veuillez recommencer encore")
        except Exception as e:
             messages.error(request, f"Une erreur a été produite {e}")

        

        return render(request, self.templates_name, self.context)
    
class AddInvoiceView(View):

    """Ajout de facture"""

    templates_name = 'add_invoices.html'
    invoices = Invoice.objects.select_related('customer', 'save_by').all()
    customers = Customer.objects.select_related('save_by').all()


    context = {
        'invoices': invoices,
        'customers': customers,
    }

    def get(self, request, *args, **kwargs):
        return render(request, self.templates_name, self.context)
    
    def post(self, request, *args, **kwargs):
        data = request.POST
        
        context = {
            "customer": data.get('customer'),
            "invoice_date_time": data.get('invoice_date_time'),
            "total": data.get('total'),
            "paid": data.get('paid'),
            "invoice_type": data.get('invoice_type'),
            "comments": data.get('comments'),
            "last_updated_date": data.get('last_updated_date'),
            "save_by": request.user
        }
        
        try:
            created = Invoice.objects.create(**context)
            if created:
                messages.success(request,"La facture a été créé avec succès")
            else:
                 messages.error(request, "Veuillez recommencer encore")
        except Exception as e:
             messages.error(request, f"Une erreur a été produite {e}")

        
        return render(request, self.templates_name, self.context)
