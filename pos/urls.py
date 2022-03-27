from django.urls import path
from .views import *


urlpatterns = []


urlpatterns += [
    path('product', ProductAPI.as_view(), name='product-end-point'),
    path('category', CategoryAPI.as_view(), name='category-end-point'),
]
