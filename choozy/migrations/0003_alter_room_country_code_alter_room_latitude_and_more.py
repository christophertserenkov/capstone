# Generated by Django 5.1 on 2024-10-17 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('choozy', '0002_room_country_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='country_code',
            field=models.CharField(max_length=2),
        ),
        migrations.AlterField(
            model_name='room',
            name='latitude',
            field=models.FloatField(default=None),
        ),
        migrations.AlterField(
            model_name='room',
            name='longitude',
            field=models.FloatField(default=None),
        ),
    ]