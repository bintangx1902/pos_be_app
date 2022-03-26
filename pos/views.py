from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializrers import *
from rest_framework import status


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
