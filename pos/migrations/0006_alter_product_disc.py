# Generated by Django 3.2.12 on 2022-03-31 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0005_alter_order_coupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='disc',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Discount price if desire : '),
        ),
    ]