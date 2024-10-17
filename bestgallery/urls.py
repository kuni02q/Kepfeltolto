from django.contrib import admin
from django.urls import path, include  # Importáld az include függvényt
from django.conf import settings
from django.conf.urls.static import static
from gallery import views


from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gallery.urls')),
   # path('accounts/', include('django.contrib.auth.urls')),  # Beépített auth URL-ek
    path('search/', views.search_images, name='search_images'),
    path('generate/', views.generate_image, name='generate_image'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)