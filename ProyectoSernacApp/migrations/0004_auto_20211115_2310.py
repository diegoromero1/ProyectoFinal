# Generated by Django 3.1 on 2021-11-16 02:10

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProyectoSernacApp', '0003_publicacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilesAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adminupload', models.FileField(upload_to='media')),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='contacto',
            name='numero',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='publicacion',
            name='contenido',
            field=ckeditor.fields.RichTextField(verbose_name='Contenido'),
        ),
    ]
