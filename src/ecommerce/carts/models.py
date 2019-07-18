from django.db import models
from django.conf import settings
from django.db.models.signals import m2m_changed, pre_save

from products.models import Product
# Create your models here.

User = settings.AUTH_USER_MODEL

class CartManager(models.Manager):

    def createNewOrGet(self, request):
        cartId = request.session.get("cartId", None)

        qs = self.get_queryset().filter(id=cartId)
        if qs.count() == 1:
            newObj = False
            cartObj = qs.first()
            print('Cart ID exists')
            if request.user.is_authenticated() and cartObj.user is None:
                cartObj.user = request.user
                cartObj.save()
        else:
            cartObj = Cart.objects.newCart(user=request.user)
            newObj = True
            request.session['cartId'] = cartObj.id 
        return cartObj, newObj

    def newCart(self, user=None):
        userObj = None
        if user is not None:
            if user.is_authenticated():
                userObj = user
        return self.model.objects.create(user=userObj)

    """ def get_queryset(self):
        return super().get_queryset().filter() """


class Cart(models.Model):
    user        = models.ForeignKey(User, null=True, blank=True)
    products    = models.ManyToManyField(Product, blank=True)
    subTotal    = models.DecimalField(default=0.00, max_digits=50, decimal_places=2)
    total       = models.DecimalField(default=0.00, max_digits=50, decimal_places=2)
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        print(action)
        products = instance.products.all()
        cartTotal = 0
        for product in products:
            cartTotal += product.price
        print(cartTotal)
        if instance.subTotal != cartTotal:
            instance.subTotal = cartTotal
            instance.save()

m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)

def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subTotal > 0:
        instance.total = instance.subTotal + 10 #* 1.08
    else:
        instance.total = 0

pre_save.connect(pre_save_cart_receiver, sender=Cart)