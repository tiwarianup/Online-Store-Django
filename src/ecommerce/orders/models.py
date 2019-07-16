from django.db import models
from django.db.models.signals import pre_save, post_save
from carts.models import Cart
from ecommerce.utils import uniqueOrderIdGenerator

# Create your models here.

# staus choices shown to the end user 
ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded')
)

class Order(models.Model):
    orderId = models.CharField(max_length=120, blank=True)
    #billingProfile  = 
    #shippingAddress =
    #billingAddress  = 
    cart    = models.ForeignKey(Cart)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shippingTotal = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)

    def __str__(self):
        return self.orderId
    
#pre save signal for Order
def pre_save_createOrderId(sender, instance, *args, **kwargs):
    if not instance.orderId:
        instance.orderId = uniqueOrderIdGenerator(instance)

pre_save.connect(pre_save_createOrderId, sender=Order)

#Generate Order Id
#Generate Order Total