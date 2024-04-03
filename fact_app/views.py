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

from django.db.models import Sum 
from django.db.models.functions import ExtractMonth
from django.http import JsonResponse

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


class StatisticView(LoginRequiredSuperuserMixim, View):
    """ cette vue permet d'obtenir des statistiques """

    template_name = 'statistic.html'

    def get_sold_data_for_year(self, year=None):

        if year:

            # Filtrer sur l'année spécifiée
            invoices = Invoice.objects.filter(invoice_date__year=year)
        else:
            invoices = Invoice.objects.all()    

        # Annotation du montant vendu par mois 
        monthly_totals = invoices.annotate(month=ExtractMonth('invoice_date')).values('month')\
            .annotate(total_amount=Sum('total')).order_by('month') # liste de dict [{'month': 1, 'total_anont':6567567}]
           
        result = [0] * 12
        for item in monthly_totals:
            result[item['month']-1] = int(item['total_amount'])    
        return result


    def get_stat_data_for_age(self, year=None):
        range_ages_list = ["0-15", "15-25", "25-35", "35-65", "+65"]
        data_ages = [Customer.objects.filter(age=range_elt).count() for range_elt in range_ages_list]

        if year:
            data_ages = [Customer.objects.filter(date__year=year, age=range_elt).count() for range_elt in range_ages_list]
        return data_ages


    def get_stat_sex(self, year=None):
        data_sexs = [Customer.objects.filter(sex=sex).count() for sex in ['M', 'F']]    
        if year:
            data_sexs = [Customer.objects.filter(date__year=year, sex=sex).count() for sex in ['M', 'F']]    

        return data_sexs


    def get(self, request, *args, **kwargs):
       
        customer = Customer.objects.all().count()
        invoice  = Invoice.objects.all().count()
        income = Invoice.objects.aggregate(Sum('total')).get('total__sum')


        monthly_data = self.get_sold_data_for_year()

        data_ages = self.get_stat_data_for_age()

        data_sexs = self.get_stat_sex()

        context = {
            'customer': customer,
            'invoice': invoice,
            'income': income,
            'monthly_data': monthly_data,
            'data_ages': data_ages,
            'data_sexs': data_sexs,
        }

        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):

        year = request.POST.get('selected_date')
        if year =='Tous' or year=='All':
            monthly_data = self.get_sold_data_for_year()

            data_ages = self.get_stat_data_for_age()

            data_sexs = self.get_stat_sex()
        else:
            monthly_data = self.get_sold_data_for_year(year=year)

            data_ages = self.get_stat_data_for_age(year=year)

            data_sexs = self.get_stat_sex(year=year)
        return JsonResponse({'monthly_data':monthly_data, 'data_ages':data_ages, 'data_sexs': data_sexs})    



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


