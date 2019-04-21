from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, FormView
from ads.forms import AdvertisementCreationForm
from users.models import Member

class HomeView(TemplateView):
    template_name = 'homepage.html'


class AdvertisementCreationView(FormView):
    form_class = AdvertisementCreationForm
    success_url = '/'
    template_name = 'advertisement_creation.html'
    def get_form_kwargs(self):
        return {**super().get_form_kwargs(), **{'user': self.get_object()}}

    def get_object(self):
        return get_object_or_404(Member, user__username=self.request.user)
