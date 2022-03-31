from django.shortcuts import get_object_or_404, redirect
from django.views.generic import *
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone

Menu = apps.get_model('pos', 'Product')
OrderItem = apps.get_model('pos', 'OrderItem')
Order = apps.get_model('pos', 'Order')


class ShowMenu(ListView):
    model = Menu
    ordering = ['-pk']
    template_name = 'demo/landing.html'
    context_object_name = 'menus'

    def get_context_data(self, **kwargs):
        context = super(ShowMenu, self).get_context_data(**kwargs)
        return context

    @method_decorator(login_required(login_url='/accounts/login'))
    def dispatch(self, request, *args, **kwargs):
        return super(ShowMenu, self).dispatch(request, *args, **kwargs)


class AddItem(View):
    def post(self, format=None, **kwargs):
        item = get_object_or_404(Menu, link=kwargs['link'])
        print(kwargs)
        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=self.request.user,
            ordered=False
        )

        order_qs = Order.objects.filter(user=self.request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.item.filter(item__link=item.link):
                order_item.quantity += 1
                order_item.save()
            else:
                order.item.add(order_item)
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(user=self.request.user, ordered_date=ordered_date)
            order.item.add(order_item)

        return redirect('/')

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(AddItem, self).dispatch(request, *args, **kwargs)


class OrderedItem(ListView):
    model = Order
    template_name = 'demo/cart.html'
    context_object_name = 'menus'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, ordered=False)[0]

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(OrderedItem, self).dispatch(request, *args, **kwargs)
