from django.conf.urls import url

from .views import ProductListView, ProductSlugView

urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', ProductSlugView.as_view(), name='detail'),
]
