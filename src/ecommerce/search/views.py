from django.shortcuts import render
from django.views.generic import ListView, DetailView

# Create your views here.
from products.models import Product
# Create your views here.

# View to see the products on search
class SearchProductView(ListView):
    template_name = "search/view.html"

    def get_context_data(self, *args,  **kwargs):
        context = super(SearchProductView, self).get_context_data(*args, **kwargs)
        context["query"] = self.request.GET.get("q")
        return context
    

    #Queryset returns featured products
    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get("q", None)
        if query is not None:
            return Product.objects.search(query)
        return Product.objects.featured()
        
        # __icontains = field contains this
        # __iexact = field is exactly equal to this

       

    