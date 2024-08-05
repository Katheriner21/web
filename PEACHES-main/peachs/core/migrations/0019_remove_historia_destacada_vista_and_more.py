# Generated by Django 4.2.8 on 2024-03-28 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_historia_destacada_vista'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historia_destacada',
            name='vista',
        ),
        migrations.AddField(
            model_name='historia_destacada',
            name='vista1',
            field=models.ManyToManyField(blank=True, related_name='vista1_d_joined', to='core.usuario', verbose_name='Vistas1'),
        ),
        migrations.AddField(
            model_name='historia_destacada',
            name='vista2',
            field=models.ManyToManyField(blank=True, related_name='vista2_d_joined', to='core.usuario', verbose_name='Vistas2'),
        ),
        migrations.AddField(
            model_name='historia_destacada',
            name='vista3',
            field=models.ManyToManyField(blank=True, related_name='vista3_d_joined', to='core.usuario', verbose_name='Vistas3'),
        ),
    ]
