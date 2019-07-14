"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from .views import homepage, contactpage, loginpage, registerpage
#from products.views import ProductFeaturedListView, ProductDetailView, ProductFeaturedDetailView

urlpatterns = [
    url(r'^$', homepage, name='home'),
    url(r'^contact/$', contactpage, name='contact'),
    url(r'^products/', include("products.urls", namespace='products')),
    url(r'^search/', include("search.urls", namespace='search')),
    url(r'^login/$', loginpage, name='login'),
    url(r'^register/$', registerpage, name='register'),
    url(r'^admin/', admin.site.urls),
    #url(r'^products/(?P<pk>\d+)/$', ProductDetailView.as_view(), name='product-details'),
    #url(r'^featured/$', ProductFeaturedListView.as_view(), name='featured'),
    #url(r'^featured/(?P<pk>\d+)/$', ProductFeaturedDetailView.as_view(), name='featured-details'),
]


if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL ,document_root=settings.MEDIA_ROOT)