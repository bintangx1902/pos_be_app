from django.urls import path
from .views import *

app_name = 'pos'

urlpatterns = [
    path('', api_landing, name='landing'),
    path('item', CartItem.as_view(), name='cart-item'),
    path('product', ProductAPI.as_view(), name='product-end-point'),
    path('category', CategoryAPI.as_view(), name='category-end-point'),
]
