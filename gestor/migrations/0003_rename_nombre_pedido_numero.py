# Generated by Django 3.2.9 on 2021-12-03 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestor', '0002_auto_20211129_1603'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pedido',
            old_name='nombre',
            new_name='numero',
        ),
    ]
