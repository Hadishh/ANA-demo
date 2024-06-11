# Generated by Django 5.0.4 on 2024-06-11 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='type',
            field=models.CharField(choices=[('joke', 'joke'), ('read book', 'read book'), ('story', 'story'), ('phone', 'phone'), ('other', 'other')], default='other', max_length=64),
        ),
    ]
