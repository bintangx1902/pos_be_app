from django.shortcuts import get_object_or_404, redirect
from django.views.generic import *
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages

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
        url = self.request.GET.get('url')
        item = get_object_or_404(Menu, link=kwargs['link'])
        amount = int(self.request.POST.get('amount'))
        xtra = self.request.POST.get('xtra')

        if not amount and not xtra:
            messages.error(self.request, "Set one, amount or the extra price!")
            return redirect('/')

        elif not amount and xtra:
            amount = 1
            xtra = float(xtra)

        elif not xtra:

            xtra = 0

        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=self.request.user,
            ordered=False,
        )

        order_qs = Order.objects.filter(user=self.request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.item.filter(item__link=item.link):
                order_item.quantity += amount
                order_item.xtra_price += xtra
                order_item.save()
            else:
                order.item.add(order_item)
                order_item.quantity = amount
                order_item.xtra_price = xtra
        else:
            order = Order.objects.create(user=self.request.user, order_date=timezone.now())
            order.item.add(order_item)
            order_item.quantity = amount
            order_item.xtra_price = xtra
        order_item.save()

        if url:
            return redirect(url)
        return redirect('/')

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(AddItem, self).dispatch(request, *args, **kwargs)


class OrderedItem(ListView):
    model = Order
    template_name = 'demo/cart.html'
    context_object_name = 'menus'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, ordered=False).first()

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(OrderedItem, self).dispatch(request, *args, **kwargs)


def remove_from_cart(request, link):
    item = get_object_or_404(Menu, link=link)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.item.filter(item__link=item.link).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order.item.remove(order_item)
            order_item.delete()
            # TODO : add messages "was removed"
        else:
            # TODO : add messages "item was not in cart"
            pass
    else:
        # TODO : add messages "don have an active order"
        pass

    return redirect('demo:cart')


def reduce_item(request, link):
    item = get_object_or_404(Menu, link=link)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.item.filter(item__link=item.link).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            if order_item.quantity == 1:
                return reverse('demo:remove', kwargs={'link': item.link})
            order_item.quantity -= 1
            order_item.save()
            # TODO : add messages "was reduced"
        else:
            # TODO : add messages "was not in cart"
            pass
    else:
        # TODO : add messages "dont have an active order"
        pass

    return redirect('demo:cart')
