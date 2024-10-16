# gallery/forms.py

from django import forms
from .models import Image, Tag, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import json

class ImageForm(forms.ModelForm):
    tags = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'name': 'tags'}),
        help_text='Add meg a címkéket.'
    )

    class Meta:
        model = Image
        fields = ['title', 'description', 'image_file', 'categories']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.uploader = self.instance.uploader  # Győződj meg róla, hogy a feltöltő be van állítva
            instance.save()
            # Címkék feldolgozása
            tags_data = self.cleaned_data.get('tags', '[]')
            try:
                tags_list = json.loads(tags_data)
            except json.JSONDecodeError:
                tags_list = []

            for tag_item in tags_list:
                tag_name = tag_item.get('value', '').strip()
                if tag_name:
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
        fields = ['birth_date']# További mezők hozzáadása
class ProfileUpdateForm(forms.ModelForm):
    favorite_tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Kedvenc címkék'
    )

    class Meta:
        model = Profile
        fields = ['bio', 'profile_image', 'favorite_tags']
