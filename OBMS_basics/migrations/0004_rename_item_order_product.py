# Generated by Django 4.0.4 on 2022-06-25 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OBMS_basics', '0003_orderitem_product_orderitem_quantity_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='item',
            new_name='product',
        ),
    ]
