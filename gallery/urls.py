from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.image_list, name='image_list'),
    path('upload/', views.image_upload, name='image_upload'),
    path('image/<int:pk>/', views.image_detail, name='image_detail'),
    path('signup/', views.signup, name='signup'),
    path('search/', views.search_images, name='search'),
    path('friend-search/', views.friend_search, name='friend_search'),
    path('account-settings/', views.account_settings, name='account_settings'),
    path('logout/', views.custom_logout, name='logout'),
    path('tags/', views.tag_list, name='tag_list'),
    path('image/<int:pk>/delete/', views.image_delete, name='image_delete'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('help/', views.help_page, name='help_page'),
    path('inbox/', views.inbox, name='inbox'),
    path('message/<int:pk>/', views.message_detail, name='message_detail'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('generate/', views.generate_image, name='generate_image'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
