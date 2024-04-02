import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .models import *
from django.contrib import messages

import pdfkit

from django.template.loader import get_template

from django.db import transaction

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .utils import pargination, get_invoice

from .decorators import *

from django.utils.translation import gettext as _


class HomeView(LoginRequiredSuperuserMixim, View):
    """Vue principale"""

    templates_name = 'index.html'
    invoices = Invoice.objects.select_related('customer', 'save_by').all().order_by('-invoice_date_time')

    context = {
        'invoices': invoices,
    }

    def get(self, request, *args, **kwargs):

        items = pargination(request, self.invoices)

        self.context['invoices'] = items

        return render(request, self.templates_name, self.context)
    

    def post(self, request, *args, **kwargs):

        # Modification de facture

        if request.POST.get('id_modified'):
            paid = request.POST.get('modified')

            try:
                obj = Invoice.objects.get(id=request.POST.get('id_modified'))

                if paid == 'True':
                    obj.paid = True
                else:
                    obj.paid = False
                obj.save()
                messages.success(request, _("La modification a été fait avec succès"))

            except Exception as e :
                messages.error(request, _(f"Une erreur est survenue lors du traitement {e}"))


        # Suppression de facture
                
        if request.POST.get('id_supprimer'):
           
            try:
                obj = Invoice.objects.get(pk=request.POST.get('id_supprimer'))
                obj.delete()
        
                messages.success(request, _("La suppression a été effectué avec succès"))

            except Exception as e :
                messages.error(request, _(f"Une erreur est survenue lors du traitement {e}"))


        items = pargination(request, self.invoices)

        self.context['invoices'] = items
        return render(request, self.templates_name, self.context)
    
class AddCustomerView(LoginRequiredSuperuserMixim, View):

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
                messages.success(request, _(f"Le client {data.get('name')} a été créé avec succès"))
            else:
                 messages.error(request, _("Veuillez recommencer encore"))
        except Exception as e:
             messages.error(request, _(f"Une erreur a été produite {e}"))

        

        return render(request, self.templates_name, self.context)
    
class AddInvoiceView(LoginRequiredSuperuserMixim, View):

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
               messages.success(request, _('ça été créé avec succès')) 
           else:
               messages.error(request, _("Désolé, essayez à nouveau"))
        except Exception as e:
                messages.error(request, _(f'Désolé une erreur est survenue {e}'))
        
        return render(request, self.templates_name, self.context)


class InvoiceVisualizationView(LoginRequiredSuperuserMixim, View):
    """ Visualiser la facture"""

    template_name = "invoice.html"

    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')

        context = get_invoice(pk)

        return render(request, self.template_name, context)


@superuser_required
def get_invoice_pdf(request, *args, **kwargs):
    """ générer un fichier pdf """

    pk = kwargs.get('pk')

    context = get_invoice(pk)

    context['date'] = datetime.datetime.today()

    #Obtenir le fichier html

    template = get_template('invoice-pdf.html')

    # render
    html = template.render(context)

    #Options du PDF

    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8'
    }

    # générer le fichier PDF

    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

    pdf = pdfkit.from_string(html, False, options, configuration=config)

    response = HttpResponse(pdf, content_type = 'application/pdf')
    
    response['Content-Disposition'] = 'attachement'

    return response

