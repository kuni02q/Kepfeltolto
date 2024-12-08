# gallery/forms.py

import json

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models

from .models import Comment, Gallery, Image, Profile, Tag


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ["name", "cover_image"]


class ImageForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all().order_by("name"),  # Itt rendezünk ABC sorrendbe
        widget=forms.SelectMultiple(
            attrs={"class": "select2-multiple", "placeholder": "Válassz címkéket"}
        ),
        required=False,
        help_text="Válaszd ki a címkéket, amelyek legjobban leírják a képet.",
    )

    class Meta:
        model = Image
        fields = ["image_file", "title", "description", "tags"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }
        help_texts = {
            "image_file": "Válaszd ki a feltölteni kívánt képfájlt.",
            "title": "Adj meg egy címet a képnek.",
            "description": "Írj egy rövid leírást a képről.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tags"].queryset = Tag.objects.all().order_by("name")


class AddImageToGalleryForm(forms.Form):
    gallery = forms.ModelChoiceField(
        queryset=Gallery.objects.none(),
        empty_label="Válassz egy galériát",
        required=True,
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["gallery"].queryset = Gallery.objects.filter(owner=user)


class SignUpForm(UserCreationForm):
    error_messages = {"password_mismatch": "A két jelszó nem egyezik meg."}
    email = forms.EmailField(required=True)
    first_name = forms.CharField(
        max_length=30, required=False, help_text="Nem kötelező."
    )
    last_name = forms.CharField(
        max_length=30, required=False, help_text="Nem kötelező."
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["birth_date", "profile_image", "bio"]  # További mezők hozzáadása


class ProfileUpdateForm(forms.ModelForm):
    favorite_tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Kedvenc címkék",
    )

    class Meta:
        model = Profile
        fields = [
            "bio",
            "profile_image",
            "favorite_tags",
        ]  # Győződj meg róla, hogy itt is 'profile_image' szerepel


class SearchForm(forms.Form):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "select2-multiple"}),
        required=False,
        label="Címkék",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tags"].queryset = Tag.objects.all()


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Add a comment..."})
    )

    class Meta:
        model = Comment
        fields = ["content", "parent"]
        labels = {"content": "", "parent": ""}
        widgets = {"parent": forms.HiddenInput()}
