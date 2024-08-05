# Generated by Django 5.0.2 on 2024-03-09 02:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usuario',
            options={'ordering': ['-created'], 'verbose_name': 'Usuario', 'verbose_name_plural': 'Usuarios'},
        ),
        migrations.AddField(
            model_name='usuario',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default='2022-01-01 12:00:00', verbose_name='Fecha de Creacion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='estado',
            field=models.CharField(choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], default='activo', max_length=20, verbose_name='Estado'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='tipo_usuario',
            field=models.CharField(choices=[('usuario', 'Usuario'), ('creador_contenido', 'Usuario creador de contenido')], default='usuario', max_length=30, verbose_name='Tipo de usuario'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='contrasena',
            field=models.CharField(max_length=128, verbose_name='Contraseña'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='fecha_nacimiento',
            field=models.DateField(verbose_name='Fecha de nacimiento'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='sexo',
            field=models.CharField(max_length=20, verbose_name='Sexo'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='usuario',
            field=models.CharField(max_length=150, unique=True, verbose_name='Usuario'),
        ),
        migrations.CreateModel(
            name='Datos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('dni', models.CharField(max_length=20)),
                ('telefono', models.CharField(max_length=20)),
                ('imagen1', models.ImageField(blank=True, null=True, upload_to='imagenes')),
                ('imagen2', models.ImageField(blank=True, null=True, upload_to='imagenes')),
                ('video', models.FileField(blank=True, null=True, upload_to='videos')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.usuario')),
            ],
            options={
                'verbose_name': 'Dato',
                'verbose_name_plural': 'Datos',
            },
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto1', models.CharField(max_length=160)),
                ('texto2', models.CharField(max_length=160)),
                ('texto3', models.CharField(max_length=160)),
                ('imagen_portada', models.ImageField(blank=True, null=True, upload_to='perfil')),
                ('imagen_perfil', models.ImageField(blank=True, null=True, upload_to='perfil')),
                ('imagen1', models.ImageField(blank=True, null=True, upload_to='perfil')),
                ('imagen2', models.ImageField(blank=True, null=True, upload_to='perfil')),
                ('imagen3', models.ImageField(blank=True, null=True, upload_to='perfil')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.usuario')),
            ],
            options={
                'verbose_name': 'Perfil',
                'verbose_name_plural': 'Perfiles',
            },
        ),
    ]