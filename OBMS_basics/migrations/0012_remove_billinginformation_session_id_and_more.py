# Generated by Django 4.1b1 on 2022-07-06 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OBMS_basics', '0011_order_delivered'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billinginformation',
            name='session_id',
        ),
        migrations.RemoveField(
            model_name='order',
            name='session_id',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='session_id',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='session_id',
        ),
    ]
