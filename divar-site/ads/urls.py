from django.urls import path
from ads.views import HomeView, AdvertisementCreationView, AdvertisementViewView, BookmarkView, MyAdsView, bookmark_ad

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('my-ads/', MyAdsView.as_view(template_name='my_ads.html'), name='my-ads'),
    path('creation/', AdvertisementCreationView.as_view(), name='create_advertisement'),
    path('view/<int:id>/', AdvertisementViewView.as_view(), name='view_advertisement'),
    path('bookmarks/', BookmarkView.as_view(), name='view_bookmarks'),
    path('ajax/bookmark_ad/', bookmark_ad, name='bookmark_ad'),
]

