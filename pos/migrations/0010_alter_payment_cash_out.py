# Generated by Django 3.2.12 on 2022-04-07 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0009_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='cash_out',
            field=models.FloatField(null=True),
        ),
    ]
