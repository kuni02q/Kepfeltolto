# gallery/forms.py

from django import forms
from .models import Image, Tag, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import json
from django.db import models
class ImageForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all().order_by('name'),  # Itt rendezünk ABC sorrendbe
        widget=forms.SelectMultiple(attrs={
            'class': 'select2-multiple',
            'placeholder': 'Válassz címkéket'
        }),
        required=False,
        help_text='Válaszd ki a címkéket, amelyek legjobban leírják a képet.'
    )

    class Meta:
        model = Image
        fields = ['image_file', 'title', 'description', 'tags']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        help_texts = {
            'image_file': 'Válaszd ki a feltölteni kívánt képfájlt.',
            'title': 'Adj meg egy címet a képnek.',
            'description': 'Írj egy rövid leírást a képről.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].queryset = Tag.objects.all().order_by('name')


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

class SearchForm(forms.Form):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2-multiple'}),
        required=False,
        label='Címkék'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].queryset = Tag.objects.all()