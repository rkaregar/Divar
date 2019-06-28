from django.contrib import admin
from ads.models import Category, Advertisement, Images, ReportAdvertisement
# Register your models here.


class ImagesInline(admin.TabularInline):
    model = Images
    fields = ['image']


class AdvertisementAdmin(admin.ModelAdmin):
    inlines = [ImagesInline]


admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(Category)
admin.site.register(Images)
admin.site.register(ReportAdvertisement)
