# Generated by Django 5.1.2 on 2024-11-04 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CityWeather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('city_name', models.CharField(max_length=64, verbose_name='Название города')),
                ('temperature', models.FloatField(verbose_name='Температура в городе')),
                ('atmospheric_pressure', models.IntegerField(verbose_name='Атмосферное давление')),
                ('wind_speed', models.FloatField(verbose_name='Скорость ветра')),
            ],
            options={
                'verbose_name': 'Погода по городу',
                'verbose_name_plural': 'Погода по городам',
            },
        ),
    ]