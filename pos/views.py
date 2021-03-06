from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializrers import *
from rest_framework import status
from rest_framework.decorators import api_view
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
import requests, datetime, jwt
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed


@api_view(['GET'])
def api_landing(request):
    data = {
        'login': '/api/login',
        'cart item': '/api/item',
        'product': '/api/product',
        'category': '/api/category',
        'delete item': '/api/delete-item',
        'reduce item': '/api/reduce-item'

    }
    a = request.build_absolute_uri()
    print(a.split('/'))
    return Response(data)


def payloads(token):
    try:
        payload = jwt.decode(token, 'secret', algorithms='HS256')
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Un Authenticated")

    return payload


def this_user(payload):
    return get_object_or_404(User, id=payload['id'])


class LoginEndPoint(APIView):
    def get(self, format=None):
        token = self.request.GET.get('token')
        if token:
            payload = payloads(token)
            user = this_user(payload)
            serializer = UserSerializer(user, many=False)
            response = Response()
            response.data = {
                'token': token,
                'user': serializer.data
            }
            return response
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, format=None):
        data = self.request.data
        username = data['username']
        password = data['password']

        user = User.objects.filter(username=username).first()
        if not user:
            raise AuthenticationFailed("user not found")
        user = get_object_or_404(User, username=username)
        if not user.check_password(password):
            raise AuthenticationFailed("Wrong password !")

        payload = {
            'id': user.id,
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token)
        response.data = {
            'token': token
        }

        return response


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
        token = self.request.GET.get('token')
        if not token:
            raise AuthenticationFailed("Authentication Failed")
        payload = payloads(token)
        user = this_user(payload)
        if not user:
            raise AuthenticationFailed("User not found ! ")

        order = Order.objects.filter(user=user, ordered=False).first()
        if order:
            order = order.item.all()

        serializer = OrderItemSerializer(order, many=True)
        return Response(serializer.data)

    def post(self, format=None, **kwargs):
        token = self.request.GET.get('token')
        if not token:
            raise AuthenticationFailed('Authentication Failed !')
        payload = payloads(token)
        user = this_user(payload)
        if not user:
            raise AuthenticationFailed("User not found !")

        data = self.request.data
        item = int(data['item'])
        amount = float(data['amount'])
        xtra = float(data['xtra'])

        item = get_object_or_404(Product, pk=item)

        if not amount and not xtra:
            return Response({"error": "amount and extra didn't declared well! "})

        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=user,
            ordered=False
        )

        order_qs = Order.objects.filter(user=user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.item.filter(item__link=item.link).exists():
                order_item.quantity += amount
                if order_item.quantity < 1 : order_item.quantity = 1
                order_item.xtra_price += xtra
                if order_item.xtra_price < 0 : order_item.xtra_price = 0
            else:
                if not amount:
                    amount = 1
                order.item.add(order_item)
                order_item.quantity = amount
                order_item.xtra_price = xtra
        else:
            # TODO : Create links
            order = Order.objects.create(user=user, order_date=timezone.now(), slug=None)
            order.item.add(order_item)
            order_item.quantity = amount
            order_item.xtra_price = xtra

        order_item.save()
        return self.get()


class RemoveItem(APIView):
    def post(self, format=None, **kwargs):
        token = self.request.GET.get('token')
        if not token:
            return AuthenticationFailed('Un Authenticated', status.HTTP_403_FORBIDDEN)
        payload = payloads(token)
        user = this_user(payload)
        if not user:
            return AuthenticationFailed('User not detected', status.HTTP_403_FORBIDDEN)

        data = self.request.data
        item = data['item']
        item = get_object_or_404(Product, pk=item)
        order_qs = Order.objects.filter(user=user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.item.filter(item__link=item.link).exists():
                order_item = OrderItem.objects.filter(item=item, user=user, ordered=False).first()
                order.item.remove(order_item)
                order_item.delete()
                # TODO : add message "was removed"
            else:
                # TODO : add message "was not in cart"
                pass
        else:
            # TODO : add message "dont have an active order"
            pass
        # return redirect(reverse('pos:cart-item') + f"?token={token}")

        serializer = ProductSerializer(item, many=False)
        response = Response()
        response.data = {
            'deleted-item': serializer.data,
        }
        response.status_code = status.HTTP_202_ACCEPTED
        return response


class ReduceItem(APIView):

    def get(self, format=None):
        token = self.request.GET.get('token')
        if not token:
            raise AuthenticationFailed("Un Authenticated", status.HTTP_403_FORBIDDEN)
        payload = payloads(token)
        user = this_user(payload)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

    def send(self, links, token, item):
        url: str = self.request.build_absolute_uri()
        uri = url.split('/')
        build = f"{uri[0]}//{uri[2]}/{uri[3]}/{links}"
        data = {'item': item}
        req = requests.post(url=build, data=data, params={'token': token})
        return req

    def post(self, format=None):
        token = self.request.GET.get('token')
        if not token:
            raise AuthenticationFailed("Un Authenticated", status.HTTP_403_FORBIDDEN)

        data = self.request.data
        user = int(data['user'])
        item = int(data['item'])
        amount = int(data['amount'])
        deleted = None

        item = get_object_or_404(Product, pk=item)
        order_qs = Order.objects.filter(user__pk=user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.item.filter(item__link=item.link).exists():
                order_item = OrderItem.objects.filter(item=item, user__pk=user, ordered=False).first()
                # TODO : if amount is left 1  delete the object
                if order_item.quantity == 1:
                    deleted = self.send("delete-item", token, item.pk)
                else:
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
        response = Response()
        if deleted is not None:
            response.data = {
                'item': serializer.data,
                'deleted-item': deleted.json(),
                'status': deleted.status_code
            }
        else:
            response.data = {
                'item': serializer.data,
            }
        return response
