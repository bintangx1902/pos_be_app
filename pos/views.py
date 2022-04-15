from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializrers import *
from rest_framework import status
from rest_framework.decorators import api_view
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
import requests


@api_view(['GET'])
def api_landing(request):
    data = {
        'product': '/api/product',
        'category': '/api/category',
        'cart item': '/api/item',
    }
    return Response(data)


class ProductAPI(APIView):
    def get(self, format=None):
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)

    def post(self, format=None):
        serializer = ProductSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status.HTTP_400_BAD_REQUEST)


class OrderItemAPI(APIView):
    def get(self, format=None):
        item = OrderItem.objects.all()
        serializer = OrderItemSerializer(item, many=True)
        return Response(serializer.data)

    def post(self):
        return


class CategoryAPI(APIView):
    def get(self, format=None):
        cate = Category.objects.all()
        serializer = CategorySerializer(cate, many=True)
        return Response(serializer.data)

    def post(self, format=None):
        name = self.request.data['name']
        category = Category()
        category.cate = name
        category.save()

        cate = Category.objects.all()
        serializer = CategorySerializer(cate, many=True)
        return Response(serializer.data)


class CartItem(APIView):
    def get(self, format=None, **kwargs):
        order = Order.objects.filter(user=self.request.user, ordered=False).first()
        if order:
            order = order.item.all()

        serializer = OrderItemSerializer(order, many=True)
        return Response(serializer.data)

    def post(self, format=None, **kwargs):
        data = self.request.data
        item = float(data['item'])
        amount = float(data['amount'])
        xtra = float(data['xtra'])

        item = get_object_or_404(Product, pk=item)

        if not amount and not xtra:
            # TODO : add messages
            return HttpResponseRedirect(reverse('/'))
        elif not amount and xtra:
            amount = 1
        elif not xtra:
            xtra = 0

        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=self.request.user,
            ordered=False
        )

        order_qs = Order.objects.filter(user=self.request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.item.filter(item__link=item.link).exists():
                order_item.quantity += amount
                order_item.xtra += xtra
            else:
                order.item.add(order_item)
                order_item.quantity = amount
                order_item.xtra = xtra
        else:
            # TODO : Create links
            order = Order.objects.create(user=self.request.user, order_date=timezone.now(), slug=None)
            order.item.add(order_item)
            order_item.quantity = amount
            order_item.xtra = xtra

        order_item.save()
        return HttpResponseRedirect(reverse('pos:cart-item'))


class RemoveItem(APIView):
    def post(self, format=None, **kwargs):
        data = self.request.data
        item = data['item']
        item = get_object_or_404(Product, pk=item)
        order_qs = Order.objecsts.filter(user=self.request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.item.filter(item__link=item.link).exists():
                order_item = OrderItem.objects.filter(item=item, user=self.request.user, ordered=False)[0]
                order.item.remove(order_item)
                order_item.delete()
                # TODO : add message "was removed"
            else:
                # TODO : add message "was not in cart"
                pass
        else:
            # TODO : add message "dont have an active order"
            pass
        return


class ReduceItem(APIView):

    def post(self, format=None):
        data = self.request.data
        user = int(data['user'])
        item = int(data['item'])
        amount = int(data['amount'])

        item = get_object_or_404(Product, pk=item)
        order_qs = Order.objects.filter(user__pk=user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.item.filter(item__link=item.link).exists():
                order_item = OrderItem.objects.filter(item=item, user__pk=user, ordered=False).first()
                # if amount is left 1  delete the object
                if amount:
                    order_item.quantity -= amount
                else:
                    order_item.quantity -= 1
                order_item.save()
            else:
                # TODO : add messages
                pass
        else:
            # TODO : add message "dont have an active order"
            pass

        # get item data

        order = Order.objects.filter(user__pk=user, ordered=False).first()
        if order:
            order = order.item.all()

        serializer = OrderItemSerializer(order, many=True)
        return Response(serializer.data)
