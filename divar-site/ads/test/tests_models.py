from django.test import TestCase
from ads.models import Advertisement, Category
from users.models import Member
from django.contrib.auth.models import User

from users.tests import create_member


def create_categories():
    vehicle = Category.objects.create(title='vehicle', level=1)

    car = Category.objects.create(title='car', level=2, parent=vehicle)
    motorcycle = Category.objects.create(title='motorcycle', level=2, parent=vehicle)

    Category.objects.create(title='sport_car', level=3, parent=car)
    Category.objects.create(title='heavy_car', level=3, parent=car)
    Category.objects.create(title='regular_motor', level=3, parent=motorcycle)


def create_dummy_ads(member):
    Advertisement.objects.create(title='pride', price=500, is_urgent=True, description='good car',
                                 state='Tehran', city='Tehran', user=member,
                                 category=Category.objects.get(title='sport_car'))

    Advertisement.objects.create(title='peugeot', price=1000, is_urgent=False, description='good peugeot',
                                 state='Tehran', city='Tehran', user=member,
                                 category=Category.objects.get(title='sport_car'))

    Advertisement.objects.create(title='truck', price=1500, is_urgent=False, description='ok truck',
                                 state='Tehran', city='Varamin', user=member,
                                 category=Category.objects.get(title='heavy_car'))


class AdvertisementModelTest(TestCase):
    def setUp(self):
        create_categories()
        self.member = create_member(username='test', password='test')
        self.pride_car = Advertisement.objects.create(title='pride', price=1000, is_urgent=False,
                                                      description='good car',
                                                      state='Tehran', city='Tehran', user=self.member,
                                                      category=Category.objects.get(title='sport_car'))

    def test_ad_similarity_only_one_ad(self):
        self.assertListEqual(self.pride_car.top_similar_ads(10), [])

    def test_ad_similarity_two_ads(self):
        peugeot = Advertisement.objects.create(title='peugeot', price=1000, is_urgent=False, description='good car',
                                               state='Tehran', city='Tehran', user=self.member,
                                               category=Category.objects.get(title='sport_car'))

        self.assertListEqual(self.pride_car.top_similar_ads(10), [peugeot])

    def test_ad_similarity_multiple_ads(self):
        peugeot = Advertisement.objects.create(title='peugeot', price=1000, is_urgent=False, description='good car',
                                               state='Tehran', city='Tehran', user=self.member,
                                               category=Category.objects.get(title='sport_car'))

        truck = Advertisement.objects.create(title='truck', price=1500, is_urgent=False, description='ok truck',
                                             state='Tehran', city='Varamin', user=self.member,
                                             category=Category.objects.get(title='heavy_car'))

        motor = Advertisement.objects.create(title='motor', price=500, is_urgent=True, description='ok motor',
                                             state='Kerman', city='Rafsanjan', user=self.member,
                                             category=Category.objects.get(title='heavy_car'))

        self.assertListEqual(self.pride_car.top_similar_ads(10), [peugeot, truck, motor])
