# Generated by Django 4.2.8 on 2024-03-27 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_historia_vista'),
    ]

    operations = [
        migrations.AddField(
            model_name='historia_destacada',
            name='vista',
            field=models.ManyToManyField(blank=True, related_name='vista_d_joined', to='core.usuario', verbose_name='Vistas'),
        ),
    ]