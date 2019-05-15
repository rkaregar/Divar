from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from ads.views import HomeView, AdvertisementCreationView, AdvertisementViewView, BookmarkView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('creation/', AdvertisementCreationView.as_view(), name='create_advertisement'),
    path('view/<int:id>/', AdvertisementViewView.as_view(), name='view_advertisement'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
