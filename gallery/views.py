# views.py
import base64
import os
import uuid

# import requests
import openai
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    AddImageToGalleryForm,
    CommentForm,
    GalleryForm,
    ImageForm,
    ProfileForm,
    ProfileUpdateForm,
    SearchForm,
    SignUpForm,
)
from .models import Comment, FavoriteImage, Gallery, Image, Message, Profile, Tag


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
    form = CommentForm()

    # Hozzáadás a galériához form kezelése
    gallery_form = AddImageToGalleryForm(
        user=request.user
    )  # Az aktuális felhasználó galériáit tartalmazza

    if request.method == "POST":
        if "gallery_form" in request.POST:  # Ha a galéria form kerül elküldésre
            gallery_form = AddImageToGalleryForm(user=request.user, data=request.POST)
            if gallery_form.is_valid():
                gallery = gallery_form.cleaned_data["gallery"]
                image.gallery = gallery
                image.save()
                return redirect(
                    "image_detail", pk=image.id
                )  # Galéria hozzáadás után vissza a képtörzs oldalra
        else:  # Ha a komment form kerül elküldésre
            form = CommentForm(request.POST)
            if form.is_valid():
                parent = form.cleaned_data.get("parent")
                parent_obj = None
                if parent:
                    parent_obj = Comment.objects.get(id=parent.id)
                comment = form.save(commit=False)
                comment.image = image
                comment.user = request.user
                comment.parent = parent_obj
                comment.save()

                # Értesítés küldése
                recipient = image.uploader
                if parent_obj and parent_obj.user != request.user:
                    recipient = parent_obj.user
                if recipient != request.user:
                    Message.objects.create(
                        sender=request.user,
                        recipient=recipient,
                        message_type="comment",
                        related_image=image,
                        subject="",
                        body="",
                    )
                return redirect("image_detail", pk=image.id)

    comments = image.comments.filter(parent=None)
    return render(
        request,
        "gallery/image_detail.html",
        {
            "image": image,
            "comments": comments,
            "form": form,
            "gallery_form": gallery_form,  # A galéria formot is átadjuk a sablonnak
        },
    )


@login_required
def like_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    user = request.user

    # Ha a felhasználó dislike-olta a képet, először azt eltávolítjuk
    if user in image.dislikes.all():
        image.dislikes.remove(user)

    # Ha a felhasználó még nem like-olta a képet
    if user not in image.likes.all():
        image.likes.add(user)

        # Ha a kép a "Tetszik" galériában van, hozzáadjuk
        liked_gallery = Gallery.objects.filter(name="Tetszik", owner=user).first()
        if liked_gallery:
            image.gallery = liked_gallery  # A kép hozzáadása a galériához
            image.save()

        # Üzenet küldése a feltöltőnek
        if image.uploader != user:
            Message.objects.create(
                sender=user,
                recipient=image.uploader,
                message_type="like",
                related_image=image,
                subject="",
                body="",
            )

    else:
        image.likes.remove(user)

        # Ha a kép a "Tetszik" galériában van, eltávolítjuk
        liked_gallery = Gallery.objects.filter(name="Tetszik", owner=user).first()
        if liked_gallery:
            try:
                image.gallery.remove(liked_gallery)
                image.save()
            except Exception as e:
                print(f"Error removing image from 'Tetszik' gallery: {e}")

    return redirect("image_detail", pk=image_id)


@login_required
def dislike_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)

    # Ha a felhasználó már kedvelte a képet, akkor eltávolítjuk a like-t
    if request.user in image.likes.all():
        image.likes.remove(request.user)

        # Ha eltávolítja a like-ot, akkor eltávolítjuk a képet a "Tetszik" galériából
        liked_gallery = Gallery.objects.filter(
            name="Tetszik", user=request.user
        ).first()
        if liked_gallery:
            liked_gallery.images.remove(
                image
            )  # Eltávolítjuk a képet a "Tetszik" galériából

    # Ha a felhasználó még nem dislike-olta a képet, akkor hozzáadjuk a dislikes-hoz
    if request.user not in image.dislikes.all():
        image.dislikes.add(request.user)

        # Üzenet küldése a feltöltőnek, ha másik felhasználó nem kedvelte a képet
        if image.uploader != request.user:
            Message.objects.create(
                sender=request.user,
                recipient=image.uploader,
                subject="Új 'Nem tetszik' reakció a képedre",
                body=f"{request.user.username} nem kedvelte a képedet: {image.title}. ",
            )
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
    galleries = Gallery.objects.filter(owner=user)

    # Profil frissítése
    if request.method == "POST" and "profile_form" in request.POST:
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "A profilod frissítve lett.")
            return redirect("account_settings")
    else:
        profile_form = ProfileUpdateForm(instance=profile)

    # Új galéria létrehozása
    if request.method == "POST" and "gallery_form" in request.POST:
        gallery_form = GalleryForm(request.POST, request.FILES)
        if gallery_form.is_valid():
            gallery = gallery_form.save(commit=False)
            gallery.owner = user
            gallery.save()
            messages.success(request, "Új galéria sikeresen létrehozva!")
            return redirect("account_settings")
    else:
        gallery_form = GalleryForm()

    return render(
        request,
        "gallery/account_settings.html",
        {
            "profile_form": profile_form,
            "gallery_form": gallery_form,
            "images": images,
            "galleries": galleries,
        },
    )


def gallery_detail(request, pk):
    gallery = get_object_or_404(Gallery, pk=pk)
    images = gallery.images.all()  # A galéria képeinek lekérése
    return render(
        request, "gallery/gallery_detail.html", {"gallery": gallery, "images": images}
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


def add_comment(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.image = image
            comment.user = request.user
            comment.save()

    else:
        form = CommentForm()
    return render(request, "gallery/image_detail.html", {"form": form, "image": image})


@login_required
def inbox_view(request):
    messages = Message.objects.filter(recipient=request.user).order_by("-sent_at")
    # Az összes üzenetet olvasottként jelöljük
    messages.update(is_read=True)
    return render(request, "gallery/inbox.html", {"messages": messages})


@login_required
def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk, recipient=request.user)
    # Jelöljük az üzenetet olvasottként
    if not message.is_read:
        message.is_read = True
        message.save()
    return render(request, "gallery/message_detail.html", {"message": message})


def help_page(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message_content = request.POST.get("message")

        # Üzenet küldése emailben (vagy más feldolgozás)
        send_mail(
            f"Segítségkérés - {name}",
            message_content,
            email,
            ["admin@example.com"],  # Itt add meg az admin email címét
            fail_silently=False,
        )

        messages.success(
            request, "Üzenetedet elküldtük. Hamarosan felvesszük veled a kapcsolatot."
        )
        return redirect("help_page")

    return render(request, "gallery/help_page.html")


def load_more_images(request):
    page = request.GET.get("page", 1)
    images_list = Image.objects.all().order_by("-uploaded_at")
    paginator = Paginator(images_list, 20)  # Oldalanként 20 kép
    page_obj = paginator.get_page(page)

    images_data = []
    for img in page_obj.object_list:
        images_data.append(
            {"id": img.id, "url": img.image_file.url, "title": img.title}
        )

    data = {
        "images": images_data,
        "has_next": page_obj.has_next(),
        "next_page": page_obj.next_page_number() if page_obj.has_next() else None,
    }
    return JsonResponse(data)
