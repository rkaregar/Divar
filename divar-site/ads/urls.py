from django.urls import path
from ads.views import HomeView, AdvertisementCreationView, AdvertisementViewView, BookmarkView, MyAdsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('my-ads/', MyAdsView.as_view(template_name='my_ads.html'), name='my-ads'),
    path('creation/', AdvertisementCreationView.as_view(), name='create_advertisement'),
    path('view/<int:id>/', AdvertisementViewView.as_view(), name='view_advertisement'),
    path('bookmarks/', BookmarkView.as_view(), name='view_bookmarks'),
]

