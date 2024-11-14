import base64
import os
import uuid

import openai
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    CommentForm,
    ImageForm,
    ProfileForm,
    ProfileUpdateForm,
    SearchForm,
    SignUpForm,
)
from .models import Comment, FavoriteImage, Image, Message, Profile, Tag


def image_list(request):
    images = Image.objects.all().order_by("-uploaded_at")
    return render(request, "gallery/image_list.html", {"images": images})


@login_required
def image_upload(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.uploader = request.user
            image.save()
            form.save_m2m()  # Mivel ManyToMany mezőt használunk, szükséges a form.save_m2m()
            return redirect("image_detail", pk=image.pk)
    else:
        form = ImageForm()
    return render(request, "gallery/image_upload.html", {"form": form})


def image_detail(request, pk):
    image = get_object_or_404(Image, pk=pk)
    comments = image.comments.all()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.image = image
            comment.user = request.user
            comment.save()
            return redirect("image_detail", pk=image.id)
    else:
        form = CommentForm()

    return render(
        request,
        "gallery/image_detail.html",
        {
            "image": image,
            "comments": comments,
            "form": form,
        },
    )


@login_required
def like_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    if (
        request.user in image.dislikes.all()
    ):  # nem lehet egyszerre like-olni és dislike-olni egy képet, ezért ha már dislikeolva volt, onnan eltávolítja
        image.dislikes.remove(request.user)
    if request.user not in image.likes.all():
        image.likes.add(request.user)
    else:
        image.likes.remove(request.user)
    return redirect("image_detail", pk=image_id)


@login_required
def dislike_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    if (
        request.user in image.likes.all()
    ):  # nem lehet egyszerre like-olni és dislike-olni egy képet, ezért ha már likeolva volt, onnan eltávolítja
        image.likes.remove(request.user)
    if request.user not in image.dislikes.all():
        image.dislikes.add(request.user)
    else:
        image.dislikes.remove(request.user)
    return redirect("image_detail", pk=image_id)


@login_required
def image_delete(request, pk):
    image = get_object_or_404(Image, pk=pk)

    if image.uploader != request.user:
        return redirect("image_list")

    if request.method == "POST":
        image.delete()
        messages.success(request, "A kép sikeresen törölve lett.")
        return redirect("account_settings")

    return redirect("account_settings")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Profil létrehozása, ha nem létezik
            profile, created = Profile.objects.get_or_create(user=user)
            login(request, user)
            return redirect("image_list")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def account_settings(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    images = Image.objects.filter(uploader=user).order_by("-uploaded_at")

    if request.method == "POST":
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "A profilod frissítve lett.")
            return redirect("account_settings")
    else:
        profile_form = ProfileUpdateForm(instance=profile)
    return render(
        request,
        "gallery/account_settings.html",
        {"profile_form": profile_form, "images": images},
    )


@login_required
def friend_search(request):
    query = request.GET.get("q")
    users = User.objects.exclude(id=request.user.id)
    if query:
        users = users.filter(
            Q(username__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
        )
        # Ha azt akarjuk, hogy ha üresen hagyjuk a keresési mezőt, ne dobjon egyetlen felhasználót se, akkor el kell tüntetni a kommentet:
    """else:
        users = User.objects.none()  # Üres queryset, ha nincs keresési feltétel"""
    return render(
        request, "gallery/friend_search.html", {"users": users, "query": query}
    )


def search_images(request):
    if request.method == "GET":
        form = SearchForm(request.GET)
        images = Image.objects.all()
        if form.is_valid():
            selected_tags = form.cleaned_data.get("tags")
            if selected_tags:
                images = images.filter(tags__in=selected_tags).distinct()
            else:
                images = Image.objects.none()
        else:
            images = Image.objects.none()
    else:
        form = SearchForm()
        images = Image.objects.none()

    return render(request, "gallery/search.html", {"images": images, "form": form})


def generate_image(request):
    if request.method == "POST":
        prompt = request.POST.get("prompt")
        openai.api_key = settings.OPENAI_API_KEY

        try:
            # Kép generálása az OpenAI API-val
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="512x512",
                response_format="b64_json",  # Új paraméter
            )
            image_data = base64.b64decode(response["data"][0]["b64_json"])

            filename = f"{uuid.uuid4()}.png"
            filepath = os.path.join(settings.MEDIA_ROOT, "generated", filename)

            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            with open(filepath, "wb") as f:
                f.write(image_data)

            new_image = Image.objects.create(
                title=prompt,
                image_file=f"generated/{filename}",
                uploaded_by=request.user,
            )

            return render(request, "gallery/generate_image.html", {"image": new_image})

        except Exception as e:
            return render(request, "gallery/generate_image.html", {"error": str(e)})

    return render(request, "gallery/generate_image.html")


def custom_logout(request):
    logout(request)
    return redirect("/login/")


def tag_list(request):
    q = request.GET.get("q", "")
    tags = Tag.objects.filter(name__icontains=q).order_by("name")
    tags_json = [{"id": tag.id, "name": tag.name} for tag in tags]
    return JsonResponse(tags_json, safe=False)


def help_page(request):
    return render(request, "gallery/help_page.html")


@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user).order_by("-sent_at")
    return render(request, "gallery/inbox.html", {"messages": messages})


@login_required
def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk, recipient=request.user)
    # Jelöljük az üzenetet olvasottként
    if not message.is_read:
        message.is_read = True
        message.save()
    return render(request, "gallery/message_detail.html", {"message": message})


@login_required
def add_to_favorites(request, image_id):
    image = Image.objects.get(pk=image_id)
    FavoriteImage.objects.get_or_create(user=request.user, image=image)
    return redirect("image_detail", pk=image_id)


@login_required
def remove_from_favorites(request, image_id):
    image = Image.objects.get(pk=image_id)
    FavoriteImage.objects.filter(user=request.user, image=image).delete()
    return redirect("image_detail", pk=image_id)


@login_required
def profile_edit(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect("account_settings")
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, "gallery/profile_edit.html", {"form": form})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    images = user.uploaded_images.all()
    return render(
        request, "gallery/users_profile.html", {"profile_user": user, "images": images}
    )
