# Generated by Django 3.0.5 on 2020-05-01 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200501_0321'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='street',
            field=models.BigIntegerField(default=0),
        ),
    ]
