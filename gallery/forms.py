# gallery/forms.py

from django import forms
from .models import Image, Tag, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import json
from django.db import models
class ImageForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Címkék vesszővel elválasztva'}),
        help_text='Válaszd el a címkéket vesszővel.'
    )

    class Meta:
        model = Image
        fields = ['image_file', 'title', 'description', 'tags']

    def save(self, commit=True):
        instance = super().save(commit=False)
        tags_str = self.cleaned_data.get('tags', '')
        tags_list = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
        if commit:
            instance.save()
            for tag_name in tags_list:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                instance.tags.add(tag)
        return instance

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False, help_text='Nem kötelező.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Nem kötelező.')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['birth_date','profile_image', 'bio']# További mezők hozzáadása
class ProfileUpdateForm(forms.ModelForm):
    favorite_tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Kedvenc címkék'
    )

    class Meta:
        model = Profile
        fields = ['bio', 'profile_image', 'favorite_tags']  # Győződj meg róla, hogy itt is 'profile_image' szerepel
