from django.urls import path
from .views import *


app_name = 'demo'


urlpatterns = [
    path('', ShowMenu.as_view(), name='landing'),
    path('cart', OrderedItem.as_view(), name='cart'),
    path('cart/reduce/<slug:link>', reduce_item, name='reduce'),
    path('cart/remove/<slug:link>', remove_from_cart, name='remove'),
    path('add-item/<slug:link>', AddItem.as_view(), name='add-item'),
    path('pay/<slug:slug>', SetPayment.as_view(), name='payment'),
]
