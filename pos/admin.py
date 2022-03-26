from django.contrib.admin import site
from .models import UserProfile, Product, OrderItem, Order, Coupon


site.register(UserProfile)
site.register(Product)
site.register(OrderItem)
site.register(Order)
site.register(Coupon)
