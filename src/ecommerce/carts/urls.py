from django.conf.urls import url

from .views import cartHome, cartUpdate, checkoutHome

urlpatterns = [
    url(r'^$', cartHome, name='home'),
    url(r'^update/$', cartUpdate, name='update'),
    url(r'^checkout/$', checkoutHome, name='checkout'),
]
