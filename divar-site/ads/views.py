from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseForbidden, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, CreateView, UpdateView, View
from ads.forms import AdvertisementCreationForm, ImagesFormset
from django.shortcuts import get_object_or_404
from ads.models import Advertisement, Images
from django.db import transaction


class HomeView(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['ads'] = []
        ads = Advertisement.objects.all()
        for ad in ads:
            images = Images.objects.filter(advertisement=ad.id)
            if len(images) != 0:
                image = images[0]
            else:
                image = ''
            context['ads'].append({'name': ad.title, 'info': ad.description, 'id': ad.id, 'image': image})

        context['ads'] += [{'name': 'آگهی اول', 'info': 'محصول', 'id': 1, 'image': ''},
                           {'name': 'دومین آگهی', 'info': 'توضیح', 'id': 1, 'image': ''},
                           {'name': 'دومین آگهی', 'info': 'توضیح', 'id': 1, 'image': ''},
                           {'name': 'دومین آگهی', 'info': 'توضیح', 'id': 1, 'image': ''},
                           {'name': 'دومین آگهی', 'info': 'توضیح', 'id': 1, 'image': ''}, ]
        return context


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

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied()
        self.member = request.user.member
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        advertisement_id = self.kwargs['id']
        advertisement = get_object_or_404(Advertisement, id=advertisement_id)
        context['id'] = advertisement_id
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
        context['images'] = Images.objects.filter(advertisement=advertisement_id)
        if not self.member.bookmarked_ads.filter(pk=advertisement_id):
            context['bookmark'] = 0
        else:
            context['bookmark'] = 1

        return context


class AdvertisementArchiveView(UpdateView):
    model = Advertisement
    fields = ['is_archived']

    def get_object(self, queryset=None):
        ret = super().get_object()
        if self.request.user.is_superuser or ret.user == self.request.user:
            return ret
        raise PermissionDenied()


class BookmarkView(TemplateView):
    template_name = 'bookmarked_ads.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied()
        self.member = request.user.member
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['ads'] = []
        ads = self.member.bookmarked_ads.all()
        for ad in ads:
            images = Images.objects.filter(advertisement=ad.id)
            if len(images) != 0:
                image = images[0]
            else:
                image = ''
            context['ads'].append({'name': ad.title, 'info': ad.description, 'id': ad.id, 'image': image})


        return context


def bookmark_ad(request):
    member = request.user.member
    ad_pk = request.GET['ad']
    ad = get_object_or_404(Advertisement, pk=ad_pk)
    if request.GET['bookmark'] == 'true':
        if not member.bookmarked_ads.filter(pk=ad_pk):
            member.bookmarked_ads.add(ad)
    else:
        if member.bookmarked_ads.filter(pk=ad_pk):
            member.bookmarked_ads.remove(ad)
    return JsonResponse({'result': 'ok'})


class MyAdsView(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['ads'] = []
        ads = Advertisement.objects.all()
        for ad in ads:
            images = Images.objects.filter(advertisement=ad.id)
            if len(images) != 0:
                image = images[0]
            else:
                image = ''
            context['ads'].append({'name': ad.title, 'info': ad.description, 'id': ad.id, 'image': image})

        context['ads'] += [{'name': 'آگهی اول', 'info': 'محصول', 'id': 1, 'image': ''},
                           {'name': 'دومین آگهی', 'info': 'توضیح', 'id': 1, 'image': ''},
                           {'name': 'دومین آگهی', 'info': 'توضیح', 'id': 1, 'image': ''},
                           {'name': 'دومین آگهی', 'info': 'توضیح', 'id': 1, 'image': ''},
                           {'name': 'دومین آگهی', 'info': 'توضیح', 'id': 1, 'image': ''}, ]
        return context
