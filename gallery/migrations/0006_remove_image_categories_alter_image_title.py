# Generated by Django 5.1.1 on 2024-11-03 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0005_favoriteimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='categories',
        ),
        migrations.AlterField(
            model_name='image',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
