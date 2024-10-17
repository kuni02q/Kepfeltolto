from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Image(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image_file = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category', blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    favorite_tags = models.ManyToManyField(Tag, blank=True)
    birth_date = models.DateField(blank=True, null=True)  # Hozzáadva

    def __str__(self):
        return f"{self.user.username} profilja"


class Message(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)
