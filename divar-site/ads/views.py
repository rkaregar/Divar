from django.core.exceptions import PermissionDenied
from django.http.response import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from ads.forms import AdvertisementCreationForm, ImagesFormset, ReportCreation
from django.shortcuts import get_object_or_404
from ads.models import Advertisement, Images, ReportAdvertisement, Category
from django.db import transaction

from users.models import Member


class HomeView(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            if not hasattr(self.request.user, 'member'):
                member = Member(user=self.request.user)
                member.save()
                self.request.user.member = member

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

        return context


class AdvertisementCreationView(CreateView):
    model = Advertisement
    form_class = AdvertisementCreationForm
    success_url = '/'
    template_name = 'create_ad.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['cats'] = Category.objects.filter(level=1)

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
        self.user = request.user
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
        if self.user.is_authenticated and self.user.member.bookmarked_ads.filter(pk=advertisement_id):
            context['bookmark'] = 1
        else:
            context['bookmark'] = 0

        return context


class AdvertisementArchiveView(UpdateView):
    model = Advertisement
    fields = ['is_archived']
    success_url = reverse_lazy('ads:my-ads')

    def get_object(self, queryset=None):
        ret = get_object_or_404(Advertisement, id=self.request.POST['id'])
        if self.request.user.is_superuser or ret.user == self.request.user.member:
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
            context['ads'].append(
                {'name': ad.title, 'info': ad.description, 'id': ad.id, 'image': image, 'is_archived': ad.is_archived})

        return context


class ReportCreationView(CreateView):
    model = ReportAdvertisement
    form_class = ReportCreation

    def get_success_url(self):
        return reverse('ads:view_advertisement', args=self.request.POST['id'])


class AdvertisementEditView(UpdateView):
    model = Advertisement
    fields = ['title', 'price', 'description', 'is_urgent', 'city']
    success_url = '/'
    template_name = "edit_ad.html"

    def get_object(self, queryset=None):
        ret = get_object_or_404(Advertisement, id=self.kwargs['id'])
        self.ad = ret
        if ret.user != self.request.user.member:
            raise PermissionDenied()
        return ret

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad'] = self.ad
        return context

    def form_valid(self, form):
        ad = form.save(commit=False)
        ad.user = self.request.user.member
        ad.save()
        return super().form_valid(form)


class CategoryDropdownView(View):
    def get(self, request, *args, **kwargs):
        parent_id = int(request.GET.get('parent_id', 0))
        queryset = Category.objects.filter(parent_id=parent_id)
        return HttpResponse(render_to_string('cat_dd.html', {'cats': queryset}))