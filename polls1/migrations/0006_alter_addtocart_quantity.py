# Generated by Django 4.2.7 on 2024-06-25 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls1', '0005_alter_addtocart_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addtocart',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
