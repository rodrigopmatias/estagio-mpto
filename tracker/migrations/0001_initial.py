# Generated by Django 3.2 on 2021-04-19 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nome')),
                ('abbreviation', models.CharField(max_length=2, unique=True, verbose_name='Sigla')),
            ],
        ),
    ]
