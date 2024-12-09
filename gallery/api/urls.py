from django.urls import path

from .views import AddComment, GalleryDetail, GalleryList, ImageDetail, ImageList

urlpatterns = [
    path("images/", ImageList.as_view(), name="image_list"),  # Az API végpont
    path("api/images/<int:pk>/", ImageDetail.as_view(), name="image_detail"),
    path("api/galleries/", GalleryList.as_view(), name="gallery_list"),
    path("api/galleries/<int:pk>/", GalleryDetail.as_view(), name="gallery_detail"),
    path(
        "api/images/<int:image_id>/comments/",
        AddComment.as_view(),
        name="add_comment",
    ),
]
