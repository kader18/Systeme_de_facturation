from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)
from .models import *

def pargination(request, invoices):
    # Gérer la pargination de la page
        
        # Default page

        default_page = 1

        page = request.GET.get('page', default_page)

        #Paginate items
        items_per_page = 5

        paginator = Paginator(invoices, items_per_page)

        try:
            items_page = paginator.page(page)

        except PageNotAnInteger:

            items_page = paginator.page(default_page)

        except EmptyPage:

            items_page = paginator.page(paginator.num_pages)

        return items_page

def get_invoice(pk):
    
    """Affichage de la facture"""
        
    obj = Invoice.objects.get(pk=pk)

    # Récupérer tous les articles lié à la facture
    articles = obj.article_set.all()

    context = {
        'obj': obj,
        'articles': articles
    }

    return context