# Generated by Django 2.0.2 on 2019-06-22 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0002_auto_20190616_1429'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderinfo',
            old_name='order_count',
            new_name='order_mount',
        ),
    ]