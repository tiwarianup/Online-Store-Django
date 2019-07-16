from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save

from ecommerce.utils import uniqueSlugGenerator
from products.models import Product

# Create your models here.

class Tag(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.title
    


def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    print(instance)
    if not instance.slug:
        instance.slug = uniqueSlugGenerator(instance)

pre_save.connect(tag_pre_save_receiver, sender=Tag)
