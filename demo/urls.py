from django.urls import path
from .views import *


app_name = 'demo'


urlpatterns = [
    path('', ShowMenu.as_view(), name='landing'),
    path('add-item/<slug:link>', AddItem.as_view(), name='add-item'),
]
