# Generated by Django 3.0.5 on 2020-04-09 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200409_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
    ]
