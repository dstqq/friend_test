# Generated by Django 3.1.3 on 2022-04-15 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_customuser_is_connect_to_telegram'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='connect_telegram_form',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Confirm telegram'),
        ),
    ]
