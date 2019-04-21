from django.urls import path
from ads.views import HomeView, AdvertisementCreationView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('creation/', AdvertisementCreationView.as_view(), name='create_advertisement')
]
