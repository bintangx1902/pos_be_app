from django import forms
from django.apps import apps

Payment = apps.get_model('pos', 'Payment')


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['cash_in']
