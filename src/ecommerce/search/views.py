from django.shortcuts import render
from django.views.generic import ListView, DetailView

# Create your views here.
from products.models import Product
# Create your views here.

class SearchProductView(ListView):
    template_name = "search/view.html"

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get("q", None)
        if query is not None:
            return Product.objects.filter(title__icontains=query)
        return Product.objects.featured()
        
        # __icontains = field contains this
        # __iexact = field is exactly equal to this

       

    