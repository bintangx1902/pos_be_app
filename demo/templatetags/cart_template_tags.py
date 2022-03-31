from django import template
from django.apps import apps

Order = apps.get_model('pos', 'Order')
count: int
register = template.Library()


@register.filter
def item_counter(user):
    global count
    if user.is_authenticated:
        count = 0
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            qs = qs[0]
            for item in qs.item.all():
                count += item.quantity
        return count
    return 0
