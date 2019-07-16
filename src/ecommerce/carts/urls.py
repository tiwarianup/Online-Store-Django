from django.conf.urls import url

from .views import cartHome, cartUpdate

urlpatterns = [
    url(r'^$', cartHome, name='home'),
    url(r'^update/$', cartUpdate, name='update'),
]
