# Generated by Django 2.1.7 on 2019-02-17 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fruitsales', '0002_auto_20190217_0008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='amount',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='sale',
            name='number',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='sale',
            name='sold_at',
            field=models.DateTimeField(null=True),
        ),
    ]