# Generated by Django 2.1.7 on 2019-02-16 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fruits', '0001_initial'),
        ('fruitsales', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='fruit_name',
        ),
        migrations.AddField(
            model_name='sale',
            name='fruit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fruits.Fruit'),
        ),
    ]