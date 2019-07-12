from django.shortcuts import render, Http404, get_object_or_404
from django.views.generic import ListView, DetailView

# Create your views here.
from .models import Product


class ProductFeaturedListView(ListView):
    #queryset = Product.objects.all()
    template_name = "products/list.html"

    def get_queryset(self, *args, **kwargs):
        return Product.objects.featured()

class ProductFeaturedDetailView(DetailView):
    queryset = Product.objects.all().featured()
    template_name = "products/featured-detail.html"

class ProductSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_object(self, *args, **kwargs):
        #request = self.request
        slug = self.kwargs.get("slug")
        obj = get_object_or_404(Product, slug=slug, isActive=True)

        # try:
        #     obj = Product.objects.get(slug=slug, isActive==True)
        # except Product.DoesNotExist:
        #     raise Http404("Not found!!")
        # except Product.MultipleObjectsReturned:
        #     qs = Product.objects.filter(slug=slug, isActive=True)
        #     return qs.first()
        return obj

    # def get_queryset(self, *args, **kwargs):
    #     return Product.objects.filter(slug=self.kwargs.get('slug'))

class ProductListView(ListView):
    #queryset = Product.objects.all()
    template_name = "products/list.html"

    def get_queryset(self, *args, **kwargs):
        return Product.objects.all()
    

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args,**kwargs)
    #     #context[""] = 
    #     return context

class ProductDetailView(DetailView):
    #queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_object(self, *args, **kwargs):
        #request = self.request
        pk = self.kwargs.get("pk")
        print(pk)
        obj = Product.objects.getById(pk)
        print(obj)
        if obj is None:
            raise Http404("The product does not exist.")
        return obj

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args,**kwargs)
        #print(context)
        #context[""] = 
        return context
