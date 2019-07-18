import decimal
from django.db import models
from django.db.models.signals import pre_save, post_save
from carts.models import Cart
from billing.models import BillingProfile
from ecommerce.utils import uniqueOrderIdGenerator

# Create your models here.

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded')
)

class Order(models.Model):
    billingProfile  = models.ForeignKey(BillingProfile)
    orderId = models.CharField(max_length=120, blank=True)
    #shippingAddress =
    #billingAddress  = 
    cart    = models.ForeignKey(Cart)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shippingTotal = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    active =  models.BooleanField(default=True)

    def __str__(self):
        return self.orderId

    def updateTotal(self):
        cartTotal = self.cart.total
        shippingTotal = self.shippingTotal
        total = cartTotal + decimal.Decimal(shippingTotal)
        self.total = total
        self.save()
        return total
    

def pre_save_createOrderId(sender, instance, *args, **kwargs):
    if not instance.orderId:
        instance.orderId = uniqueOrderIdGenerator(instance)

pre_save.connect(pre_save_createOrderId, sender=Order)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cartObj = instance
        cartId = cartObj.id
        qs = Order.objects.filter(cart__id=cartId)
        if qs.count() == 1:
            orderObj = qs.first()
            orderObj.updateTotal()

post_save.connect(post_save_cart_total, sender=Cart)

def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.updateTotal()

post_save.connect(post_save_order, sender=Order)