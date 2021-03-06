# Generated by Django 3.2 on 2022-05-04 05:53

import api.utils
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20220504_0437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(null=True, upload_to='images/', validators=[api.utils.validate_size, api.utils.validate_extension], verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='manga',
            name='genre',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='manga', to='api.genre', verbose_name='Жанр'),
        ),
        migrations.CreateModel(
            name='LightNovel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время последнего изменения')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('volumes', models.IntegerField(default=0, verbose_name='Количество томов')),
                ('chapters', models.IntegerField(default=0, verbose_name='Количество глав')),
                ('score', models.FloatField(default=0.0, verbose_name='Рейтинг')),
                ('status', models.CharField(blank=True, choices=[('ONGOING', 'Онгоинг'), ('RELEASED', 'Выпущено')], max_length=255, verbose_name='Статус')),
                ('synopsis', models.TextField(blank=True, verbose_name='Синопсис')),
                ('genre', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='light_novel', to='api.genre', verbose_name='Жанр')),
            ],
            options={
                'verbose_name': 'Ранобэ',
                'verbose_name_plural': 'Ранобэ',
            },
        ),
    ]
