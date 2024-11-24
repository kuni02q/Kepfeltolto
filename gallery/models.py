#models.py
import base64

import openai
from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    uploader = models.ForeignKey(
        User, related_name="uploaded_images", on_delete=models.CASCADE
    )
    image_file = models.ImageField(upload_to="images/")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="image_likes", blank=True)
    dislikes = models.ManyToManyField(User, related_name="image_dislikes", blank=True)

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def __str__(self):
        return self.title


class Comment(models.Model):
    image = models.ForeignKey(Image, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.content[:20]}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to="profile/", blank=True, null=True)
    favorite_tags = models.ManyToManyField(Tag, blank=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} profilja"


class Message(models.Model):
    MESSAGE_TYPE_CHOICES = [
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('message', 'Message'),
    ]

    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages', null=True, blank=True
    )
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_messages'
    )
    subject = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    message_type = models.CharField(
        max_length=10,
        choices=MESSAGE_TYPE_CHOICES,
        default='message'
    )
    related_image = models.ForeignKey(
        'Image', on_delete=models.CASCADE, null=True, blank=True, related_name='notifications'
    )

    def __str__(self):
        return f"{self.get_message_type_display()} from {self.sender} to {self.recipient}"

class FavoriteImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "image")

    def __str__(self):
        return f"{self.user.username} kedveli ezt a képet: {self.image.title}"
