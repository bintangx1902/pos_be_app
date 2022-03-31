from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(upload_to='profile/', null=True, blank=True)
    phone_number = models.CharField(max_length=255)


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    link = models.SlugField(max_length=255, unique=True)
    price = models.FloatField(verbose_name='Real Price : ')
    disc = models.FloatField(default=0, null=True, blank=True, verbose_name='Discount price if desire : ')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - Rp. {self.price}"

    def add_item_to_cart(self):
        return reverse('demo:add-item', kwargs={'link': self.link})


class Coupon(models.Model):
    code = models.SlugField(unique=True)
    discount = models.IntegerField(verbose_name='discount in percent ')

    def __str__(self):
        return self.code


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    xtra_price = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

    def get_total_item_price(self):
        if not self.xtra_price:
            return self.quantity * self.item.price
        return self.quantity * self.item.price + self.xtra_price

    def get_total_item_discount_price(self):
        if not self.xtra_price:
            return self.quantity * self.item.disc
        return self.quantity * self.item.disc + self.xtra_price

    def get_amount_saved(self):
        return (self.get_total_item_price() - self.xtra_price) - (self.get_total_item_discount_price() - self.xtra_price)

    def get_final_price(self):
        if self.item.disc:
            return self.get_total_item_discount_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ManyToManyField(OrderItem)
    order_date = models.DateTimeField(null=True, blank=True)
    ordered = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_total_amount_saved(self):
        total = 0
        for item in self.item.all():
            total += item.get_amount_saved()

    def get_total(self):
        total = 0
        for item in self.item.all():
            total += item.get_final_price()
        if self.coupon:
            discount = self.coupon.discount / 100
            total -= (total * discount)
        return total
