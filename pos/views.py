from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializrers import *


class ProductAPI(APIView):
    def get(self, format=None):
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)

    def post(self, format=None):
        return
