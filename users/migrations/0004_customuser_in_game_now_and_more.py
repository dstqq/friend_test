# Generated by Django 4.0.3 on 2022-04-09 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_customuser_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='in_game_now',
            field=models.BooleanField(default=False, verbose_name='Playing now or no'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='telegram_confirm_code',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Telegram confirm code'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='telegram_id',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Telegram ID'),
        ),
    ]
