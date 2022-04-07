# Generated by Django 3.2.12 on 2022-04-07 05:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pos', '0010_alter_payment_cash_out'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='cash_in',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pos.order'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
