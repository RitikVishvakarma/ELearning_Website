# Generated by Django 3.1.5 on 2021-04-16 08:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0002_auto_20210416_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='timeStamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='videos',
            name='timeStamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
