from django.urls import path
from ads.views import HomeView, AdvertisementCreationView, AdvertisementViewView, BookmarkView, MyAdsView, bookmark_ad, \
    AdvertisementArchiveView, ReportCreationView, AdvertisementEditView, CategoryDropdownView, search

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('my-ads/', MyAdsView.as_view(template_name='my_ads.html'), name='my-ads'),
    path('creation/', AdvertisementCreationView.as_view(), name='create_advertisement'),
    path('view/<int:id>/', AdvertisementViewView.as_view(), name='view_advertisement'),
    path('bookmarks/', BookmarkView.as_view(), name='view_bookmarks'),
    path('ajax/bookmark_ad/', bookmark_ad, name='bookmark_ad'),
    path('archive/<int:id>/', AdvertisementArchiveView.as_view(), name='archive_ad'),
    path('report/<int:id>/', ReportCreationView.as_view(), name='report_ad'),
    path('edit/<int:id>/', AdvertisementEditView.as_view(), name='edit_ad'),
    path('dropdown/', CategoryDropdownView.as_view(), name='dropdown'),
    path('search/', search, name='search'),
]
