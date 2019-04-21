from django.urls import path
from ads.views import HomeView, AdvertisementCreationView, AdvertisementViewView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('creation/', AdvertisementCreationView.as_view(), name='create_advertisement'),
    path('view/<int:id>/', AdvertisementViewView.as_view(), name='view_advertisement')
]
