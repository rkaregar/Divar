from django.urls import path
from ads.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]