from django.contrib import admin
from ads.models import Category, Advertisement, Images
# Register your models here.

admin.site.register(Advertisement)
admin.site.register(Category)
admin.site.register(Images)
