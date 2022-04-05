from django.contrib.admin import site
from .models import UserProfile, Product, OrderItem, Order, Coupon, Category, Payment


site.register(UserProfile)
site.register(Product)
site.register(Category)
site.register(OrderItem)
site.register(Order)
site.register(Coupon)
site.register(Payment)
