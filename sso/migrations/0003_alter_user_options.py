# Generated by Django 3.2 on 2022-05-04 04:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sso', '0002_alter_user_date_of_birth'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
