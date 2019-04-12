from django.contrib import admin

# Register your models here.
from users.models import Member, ActivationCode

admin.site.register(Member)
admin.site.register(ActivationCode)