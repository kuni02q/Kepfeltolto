# Generated by Django 5.1.2 on 2024-11-11 15:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0007_alter_profile_profile_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='image_dislikes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='image',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='image_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]