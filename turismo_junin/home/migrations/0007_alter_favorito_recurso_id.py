# Generated by Django 3.2.4 on 2021-07-22 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_recurso_puntuacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorito',
            name='recurso_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favoritos', to='home.recurso'),
        ),
    ]