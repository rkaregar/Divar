from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from users.models import Member
from django.db.models.deletion import CASCADE


class Advertisement(models.Model):
    title = models.CharField(max_length=20)
    price = models.IntegerField()
    is_urgent = models.BooleanField(default=False)
    description = models.CharField(max_length=200)
    is_archived = models.BooleanField(default=False)
    state = models.CharField(max_length=256, blank=True, null=True)
    city = models.CharField(max_length=256, blank=True, null=True)
    user = models.ForeignKey(to=Member, on_delete=CASCADE, related_name='member')
    creation_time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(to='Category', on_delete=CASCADE)

    def __str__(self):
        return self.title

    def ad_similarity(self, other_ad):
        score = 0

        if self.user == other_ad.user:
            score += 5

        if self.category == other_ad.category:
            score += 10
        elif self.category.parent == other_ad.category.parent:
            score += 7
        elif self.category.parent.parent == other_ad.category.parent.parent:
            score += 5

        if self.city == other_ad.city:
            score += 7
        elif self.state == other_ad.state:
            score += 5

        if self.price == other_ad.price:
            score += 2

        if self.is_urgent == other_ad.is_urgent:
            score += 1

        return score / 25.

    def top_similar_ads(self, num_of_ads):
        ads = list(Advertisement.objects.filter(~Q(pk=self.pk)))

        if len(ads) == 0:
            return []

        ads_scores = sorted(list(zip(ads, list(map(self.ad_similarity, ads)))), key=lambda x: x[1], reverse=True)
        return list(list(zip(*ads_scores))[0])[:num_of_ads]


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


class ReportAdvertisement(models.Model):
    reason = models.CharField(max_length=200, null=True, blank=True)
    advertisement = models.ForeignKey(to=Advertisement, on_delete=CASCADE, related_name='reports')

    def __str__(self):
        return self.advertisement.title
