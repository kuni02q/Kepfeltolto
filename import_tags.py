# import_tags.py

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bestgallery.settings')
django.setup()

from gallery.models import Tag
from gallery.tags_list import tags_list

for tag_name in tags_list:
    tag_name = tag_name.strip()
    if tag_name:
        tag, created = Tag.objects.get_or_create(name=tag_name)
        if created:
            print(f"Címke létrehozva: {tag_name}")
        else:
            print(f"Címke már létezik: {tag_name}")
