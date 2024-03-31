from django.shortcuts import render
from django.views import View
from .models import *
from django.contrib import messages

from django.db import transaction


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
    customers = Customer.objects.select_related('save_by').all()


    context = {
        'customers': customers,
    }

    def get(self, request, *args, **kwargs):
        return render(request, self.templates_name, self.context)
    
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        
        items = []
        try:
           customer = request.POST.get('customer')
           type = request.POST.get('invoice_type')
           articles = request.POST.getlist('article')

           qties = request.POST.getlist('qty')
           units = request.POST.getlist('unit')

           total_a = request.POST.getlist('total-a')

           total = request.POST.get('total')

           comment = request.POST.get('comment')

           invoice_object = {
               'customer_id': customer,
               'save_by': request.user,
               'total': total,
               'invoice_type': type,
               'comments': comment
           }

           invoice = Invoice.objects.create(**invoice_object)

           for item, article in enumerate(articles):
               data = Article(
                   invoice_id = invoice.id,
                   save_by = request.user,
                   name = article,
                   quantity = qties[item],
                   unit_price = units[item],
                   total = total_a[item]
               )

               items.append(data)

           created = Article.objects.bulk_create(items)

           if created:
               messages.success(request, 'ça été créé avec succès') 
           else:
               messages.error(request, "Désolé, essayez à nouveau")
        except Exception as e:
                messages.error(request, f'Désolé une erreur est survenue {e}')
        
        return render(request, self.templates_name, self.context)
