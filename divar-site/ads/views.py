from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, CreateView
from ads.forms import AdvertisementCreationForm, ImagesFormset
from django.shortcuts import get_object_or_404
from ads.models import Advertisement
from django.db import transaction

class HomeView(TemplateView):
    template_name = 'homepage.html'


class AdvertisementCreationView(CreateView):

    model = Advertisement
    form_class = AdvertisementCreationForm
    success_url = '/'
    template_name = 'create_ad.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if self.request.POST:
            data['images'] = ImagesFormset(self.request.POST, self.request.FILES)
        else:
            data['images'] = ImagesFormset()

        return data


    def get_form_kwargs(self):
        return {**super().get_form_kwargs(), **{'user': self.get_object()}}

    def form_valid(self, form):
        context = self.get_context_data()
        images = context['images']

        ret = super().form_valid(form)

        with transaction.atomic():
            # self.object = form.save(commit=False)

            if images.is_valid():
                images.instance = self.object
                images.save()

        return ret

    def get_object(self, queryset=None):
        return self.request.user.member


class AdvertisementViewView(TemplateView):
    template_name = 'view_ad.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        advertisement_id = self.kwargs['id']
        advertisement = get_object_or_404(Advertisement, id=advertisement_id)
        context['title'] = advertisement.title
        context['price'] = advertisement.price
        context['description'] = advertisement.description
        context['city'] = advertisement.city
        context['creation_time'] = advertisement.creation_time
        context['is_urgent'] = advertisement.is_urgent
        context['category'] = 'karegar'
        context['user_phone'] = advertisement.user.phone_number
        context['user_email'] = advertisement.user.email
        context['sharable_link'] = 'ads/view/' + str(advertisement_id)
        return context
