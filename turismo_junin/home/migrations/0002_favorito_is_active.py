# Generated by Django 3.2.4 on 2021-07-22 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='favorito',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]