# Generated by Django 4.2.5 on 2023-10-01 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_image'),
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(through='carts.CartProducts', to='products.product'),
        ),
    ]
