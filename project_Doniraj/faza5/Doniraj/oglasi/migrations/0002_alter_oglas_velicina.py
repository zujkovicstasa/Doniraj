# Generated by Django 4.2.13 on 2024-05-30 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oglasi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oglas',
            name='velicina',
            field=models.CharField(choices=[('bebe', 'bebe'), ('xs', 'XS'), ('s', 'S'), ('m', 'M'), ('l', 'L'), ('xl', 'XL'), ('xxl', 'XXL')], max_length=5),
        ),
    ]
