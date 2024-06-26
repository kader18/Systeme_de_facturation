from django import forms
from django.db import models
from django.contrib.auth.models import User

#Traduction
from django.utils.translation import gettext_lazy as _


class Customer(models.Model):
    """
    Name:Customer model definition

    """
    SEX_TYPES = (
        ('M', _('Masculin')),
        ('F', _('Feminin')),
    )

    name = models.CharField(max_length=132)
    email = models.EmailField()
    phone = models.CharField(max_length=130)
    address = models.CharField(max_length=64)
    sex = models.CharField(max_length=1, choices=SEX_TYPES)
    age = models.CharField(max_length=12)
    city = models.CharField(max_length=33)
    zip_code = models.CharField(max_length=16)
    create_date = models.DateTimeField(auto_now_add=True)
    save_by = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")

    def __str__(self):
        return self.name
    
class Invoice(models.Model):
    """
    Name: Invoice model definition
    Description:
    author: kadersoro18@gmail.com
    """

    INVOICE_TYPE = (
        ('R', _('Reçu')),
        ('P', _('Proforma facture')),
        ('F', _('Facture'))
    )

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    save_by = models.ForeignKey(User, on_delete=models.PROTECT)
    invoice_date_time = models.DateTimeField(auto_now_add=True)
    invoice_date = models.DateField(_("Date"), auto_now_add=True)
    total = models.DecimalField(max_digits=10000, decimal_places=2)
    last_updated_date = models.DateTimeField(null=True, blank=True)
    paid = models.BooleanField(default=False)
    invoice_type = models.CharField(max_length=1, choices=INVOICE_TYPE)

    comments = models.TextField(null=True, max_length=1000, blank=True)

    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")

    def __str__(self):
        return f'{self.customer.name}_{self.invoice_date_time}'
    
    @property
    def get_total(self):
        articles = self.article_set.all()
        total = sum(article.get_total for article in articles)
        return total
    
class Article(models.Model):
    """
    Name: Article model definition
    Description:
    author: kadersoro18@gmail.com
    """

    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT)
    save_by = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=150)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=1000, decimal_places=2)
    total = models.DecimalField(max_digits=1000, decimal_places=2)

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")

    @property
    def get_total(self):
        total = self.quantity * self.unit_price
        return total

    def __str__(self):
        return self.name
