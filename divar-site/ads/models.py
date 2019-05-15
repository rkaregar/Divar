from django.core.exceptions import ValidationError
from django.db import models
from users.models import Member
from django.db.models.deletion import CASCADE

# Create your models here.


class Advertisement(models.Model):
    city_choices = (
        ('Tehran', 'Tehran'),
        ('Rasht', 'Rasht'),
        ('Kerman', 'Kerman'),
        ('Isfahan', 'Isfahan'),
        ('Rafsanjan', 'Rafsanjan'),
        ('Birjand', 'Birjand')
    )
    title = models.CharField(max_length=20)
    price = models.CharField(max_length=10)
    is_urgent = models.BooleanField(default=False)
    description = models.CharField(max_length=200)
    is_archived = models.BooleanField(default=False)
    city = models.CharField(max_length=20, choices=city_choices)
    user = models.ForeignKey(to=Member, on_delete=CASCADE, related_name='member')
    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    level_choices = (
        (1, 'Level 1'),
        (2, 'Level 2'),
        (3, 'Level 3')
    )
    title = models.CharField(max_length=12)
    level = models.IntegerField(choices=level_choices)
    parent = models.ForeignKey(to='self', on_delete=CASCADE, related_name='children', null=True, blank=True)

    def __str__(self):
        return self.title

    def clean(self):
        if not self.parent and self.level != 1:
            raise ValidationError({'parent': 'Parent could not be null for non-level 1 categories'})
        if self.parent and self.parent.level != self.level - 1:
            raise ValidationError({'parent': 'Parent should be selected among the categories of one higher level'})

class Images(models.Model):
    image = models.ImageField(upload_to='img', null=True)
    advertisement = models.ForeignKey(to=Advertisement, on_delete=CASCADE, related_name='images')
