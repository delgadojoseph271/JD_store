# Generated by Django 4.2.5 on 2023-09-25 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_image'),
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='products',
            field=models.ManyToManyField(blank=True, to='products.product'),
        ),
    ]
