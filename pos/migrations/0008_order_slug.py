# Generated by Django 3.2.12 on 2022-04-05 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0007_alter_orderitem_xtra_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]