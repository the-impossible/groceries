# Generated by Django 4.0.4 on 2022-07-01 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OBMS_basics', '0009_rename_billinformation_billinginformation_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='billingInformation',
            new_name='billing',
        ),
        migrations.AlterField(
            model_name='payment',
            name='stripe_charge_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
