# Generated by Django 3.0.4 on 2020-04-22 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20200421_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='answer',
            field=models.CharField(default='', max_length=1024),
        ),
    ]