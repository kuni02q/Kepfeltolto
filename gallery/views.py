# gallery/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from .models import Image, Tag, Profile ,Message
from .forms import ImageForm, SignUpForm, ProfileForm ,ProfileUpdateForm

def image_list(request):
    images = Image.objects.all().order_by('-uploaded_at')
    return render(request, 'gallery/image_list.html', {'images': images})

@login_required
def image_upload(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.uploader = request.user
            image.save()
            form.save_m2m()  # ManyToMany mezők mentése
            return redirect('image_detail', pk=image.pk)
    else:
        form = ImageForm()
    return render(request, 'gallery/image_upload.html', {'form': form})

def image_detail(request, pk):
    image = get_object_or_404(Image, pk=pk)
    return render(request, 'gallery/image_detail.html', {'image': image})

@login_required
def image_delete(request, pk):
    image = get_object_or_404(Image, pk=pk)

    # Ellenőrizzük, hogy a bejelentkezett felhasználó a kép feltöltője-e
    if image.uploader != request.user:
        # Ha nem, visszairányítjuk a felhasználót egy hibaoldalra vagy a főoldalra
        return redirect('image_list')

    if request.method == 'POST':
        image.delete()
        messages.success(request, 'A kép sikeresen törölve lett.')
        # Visszairányítjuk a felhasználót a saját fiók oldalára
        return redirect('account_settings')

    # Ha valaki GET kérést küld erre az URL-re, visszairányítjuk
    return redirect('account_settings')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Létrehozzuk a felhasználó profilját
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('image_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def account_settings(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    images = Image.objects.filter(uploader=user).order_by('-uploaded_at')

    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'A profilod frissítve lett.')
            return redirect('account_settings')
    else:
        profile_form = ProfileUpdateForm(instance=profile)
    return render(request, 'gallery/account_settings.html', {
        'profile_form': profile_form,
        'images': images
    })
@login_required
def friend_search(request):
    query = request.GET.get('q')
    users = User.objects.exclude(id=request.user.id)
    if query:
        users = users.filter(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
    return render(request, 'gallery/friend_search.html', {'users': users, 'query': query})

def search(request):
    query = request.GET.get('q', '')
    images = None
    if query:
        # A '#' jel eltávolítása a keresési feltételből
        tag_name = query.lstrip('#')
        images = Image.objects.filter(tags__name__icontains=tag_name).distinct()
    return render(request, 'gallery/search.html', {'images': images, 'query': query})


def custom_logout(request):
    logout(request)
    return redirect('/login/')
def tag_list(request):
    tags = list(Tag.objects.values_list('name', flat=True))
    return JsonResponse(tags, safe=False)
def help_page(request):
    return render(request, 'gallery/help_page.html')
@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user).order_by('-sent_at')
    return render(request, 'gallery/inbox.html', {'messages': messages})
@login_required
def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk, recipient=request.user)
    # Jelöljük az üzenetet olvasottként
    if not message.is_read:
        message.is_read = True
        message.save()
    return render(request, 'gallery/message_detail.html', {'message': message})