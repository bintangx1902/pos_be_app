# Generated by Django 3.2.12 on 2022-04-02 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0006_alter_product_disc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='xtra_price',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]