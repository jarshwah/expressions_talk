from django.db import models
from django.db.models import Avg, Count, F, Func, Min, Max, Sum, Value


class Customer(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    base_cost = models.DecimalField(max_digits=10, decimal_places=2)


class Sale(models.Model):
    sale_date = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, related_name='sales')
    customer = models.ForeignKey(Customer, related_name='sales')
    discount = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True)
    tax_paid = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True)


# Our custom expression. Converts a DateTimeField into a DateField
class Date(Func):
    function = 'DATE'  # MySQL and SQLite
    output_field = models.DateField()

    def as_postgresql(self, compiler, connection):
        self.template = '(%(expression)s)::DATE'
        return super().as_sql(compiler, connection)

    def as_oracle(self, compiler, connection):
        self.function = 'TRUNC'
        return super().as_sql(compiler, connection)


def example_queries():
    from django.db.models import Count

    # Calculate the number of sales we made
    # per day. We need to reduce the sale date and time
    # down to just date for selection and for grouping. We
    # can then perform the aggregation per day without the time
    # component.
    sales_per_day = Sale.objects.annotate(
        date=Date('sale_date')
    ).values('date').aggregate(
        sales=Count('pk')
    ).order_by('date')

    for spd in sales_per_day:
        print("{date} \t {sales}".format(**spd))

    from decimal import Decimal
    from django.db.models import F
    from django.db.models.functions import Coalesce

    # Precalculate the invoice amount so that we can perform filtering
    # over the result. Return the top 5 invoice amounts below $1000.
    # Coalesce is necessary here so that possible NULL values in tax
    # and discount do not propagate and render the entire calculation
    # NULL.
    # See: https://docs.djangoproject.com/en/dev/ref/models/database-functions/#coalesce
    sales_with_invoice = Sale.objects.select_related(
        'customer, product'
    ).annotate(
        invoice=(
            F('product__base_cost') +
            Coalesce(F('tax_paid'), Decimal('0.00')) -
            Coalesce(F('discount'), Decimal('0.00'))
        )
    ).filter(
        invoice__lt=1000
    ).order_by('-invoice')[:5]

    for sale in sales_with_invoice:
        print('{} bought {} and paid ${}'.format(
            sale.customer.name, sale.product.name, sale.invoice
        ))

    from django.db.models import Case, F, When
    product_analysis = Product.objects.annotate(
        group=Case(
            When(base_cost__lt=500, then=Value('Low')),
            When(base_cost__range=(500, 1000), then=Value('Medium')),
            When(base_cost__gt=1000, then=Value('High')),
            output_field=models.CharField()
        )
    ).values(
        'group'
    ).annotate(
        sales_count=Count('sales'),
        revenue=Sum('base_cost') - F('sales__discount'),
        max_discount=Max('sales__discount'),
        avg_discount=Avg('sales__discount'),
        avg_discount_percentage=Avg(
            F('sales__discount') / F('base_cost') * 100
        ),
    )

    # do something with count of return customers vs once off customers
