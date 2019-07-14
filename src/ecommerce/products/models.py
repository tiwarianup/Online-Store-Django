import random 
import os

from django.db.models import Q
from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save

from .utils import uniqueSlugGenerator


# Create your models here.

def getFileExtenstion(filePath):
    baseName = os.path.basename(filePath)
    name, ext = os.path.splitext(baseName)
    return name, ext

def uploadImagePath(instance, filename):
    print(instance)
    print(filename)
    newFilename = random.randint(1, 4244248573053242)
    name, ext = getFileExtenstion(filename)
    uploadFilename = '{newFilename}{ext}'.format(newFilename=newFilename, ext=ext)
    return "products/{newFilename}/{uploadFilename}".format(newFilename=newFilename, uploadFilename=uploadFilename)


class ProductQuerySet(models.QuerySet):
    def featured(self):
        return self.filter(featured=True, isActive=True)
    
    def search(self, query):
        lookups = (Q(title__icontains=query) | Q(description__icontains=query) | Q(price__icontains=query))
        return self.filter(lookups).distinct()
    
    def active(self):
        return self.filter(isActive=True)

class ProductManager(models.Manager):

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def getById(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None


    def featured(self):
        return self.get_queryset().featured()

    def search(self, query):
        return self.get_queryset().active().search(query)

class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2, default=99.99)
    image = models.ImageField(upload_to=uploadImagePath, null=True, blank=True)
    featured = models.BooleanField(default=False)
    isActive = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ProductManager()

    def get_absolute_url(self):
        #return '/products/{slug}/'.format(slug=self.slug)
        return reverse("products:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = uniqueSlugGenerator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)
