# Generated by Django 3.2.7 on 2021-09-06 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='verification_code',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='subscriber',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]