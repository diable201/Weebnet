# Generated by Django 3.2 on 2022-05-04 05:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sso', '0003_alter_user_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('id',), 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
