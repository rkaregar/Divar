from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from ads.test.tests_models import create_categories, create_dummy_ads
from users.tests import create_member, login
from ads.models import Advertisement, Category, ReportAdvertisement

import time

DELAY = 3  # seconds


class AdsStaticLiveServerTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Chrome()
        super(AdsStaticLiveServerTestCase, self).setUp()
        create_categories()

        self.member = create_member('test', 'test')
        login(self.selenium, self.live_server_url, 'test', 'test')

    def tearDown(self):
        self.selenium.quit()
        super(AdsStaticLiveServerTestCase, self).tearDown()


class SearchLiveServerTestAds(AdsStaticLiveServerTestCase):
    def test_redirect_to_homepage(self):
        self.selenium.get(self.live_server_url)
        self.assertEqual(self.selenium.current_url, self.live_server_url + '/ads/')

    def test_homepage_show_ads(self):
        create_dummy_ads(self.member)
        self.selenium.get(self.live_server_url)

        try:
            WebDriverWait(self.selenium, DELAY).until(EC.presence_of_element_located((By.TAG_NAME, 'img')))
        except TimeoutException:
            print('time out')

        assert 'pride' in self.selenium.page_source
        assert 'good peugeot' in self.selenium.page_source
        assert 'ok truck' in self.selenium.page_source

    def test_search_title(self):
        create_dummy_ads(self.member)
        self.selenium.get(self.live_server_url)

        title = self.selenium.find_element_by_id('title')
        title.send_keys('pride')

        search = self.selenium.find_element_by_id('search')
        search.send_keys(Keys.RETURN)

        try:
            WebDriverWait(self.selenium, DELAY).until(EC.presence_of_element_located((By.TAG_NAME, 'img')))
        except TimeoutException:
            print('time out')

        assert 'pride' in self.selenium.page_source
        assert 'peugeot' not in self.selenium.page_source
        assert 'truck' not in self.selenium.page_source

    def test_search_price(self):  # currently does not work :?
        create_dummy_ads(self.member)
        self.selenium.get(self.live_server_url)

        price_low = self.selenium.find_element_by_id('price_low')
        price_low.send_keys('750')
        price_high = self.selenium.find_element_by_id('price_high')
        price_high.send_keys('1250')

        search = self.selenium.find_element_by_id('search')
        search.send_keys(Keys.RETURN)

        try:
            WebDriverWait(self.selenium, DELAY).until(EC.presence_of_element_located((By.TAG_NAME, 'img')))
        except TimeoutException:
            print('time out')

        # only peugeot ad is in this price range
        assert 'peugeot' in self.selenium.page_source
        assert 'pride' not in self.selenium.page_source
        assert 'truck' not in self.selenium.page_source

    def test_search_category(self):
        create_dummy_ads(self.member)
        self.selenium.get(self.live_server_url)

        select1 = Select(self.selenium.find_element_by_id("select1"))
        select2 = Select(self.selenium.find_element_by_id("select2"))
        category = Select(self.selenium.find_element_by_id("category"))

        select1.select_by_index(1)
        time.sleep(1)
        select2.select_by_index(1)
        time.sleep(1)
        category.select_by_index(2)

        search = self.selenium.find_element_by_id('search')
        search.send_keys(Keys.RETURN)

        time.sleep(1)

        # only truck is in this category
        assert 'truck' in self.selenium.page_source
        assert 'pride' not in self.selenium.page_source
        assert 'peugeot' not in self.selenium.page_source

    def test_no_results(self):
        create_dummy_ads(self.member)
        self.selenium.get(self.live_server_url)

        title = self.selenium.find_element_by_id('title')
        title.send_keys('NOT ANY ADS')  # this title does not match any ads

        search = self.selenium.find_element_by_id('search')
        search.send_keys(Keys.RETURN)

        time.sleep(1)

        assert 'آگهی‌ای پیدا نشد' in self.selenium.page_source


class AdLiveServerTestAds(AdsStaticLiveServerTestCase):
    def create_ad_and_move_to_my_ads(self):
        Advertisement.objects.create(title='pride', price=500, is_urgent=True, description='good car',
                                     state='Tehran', city='Tehran', user=self.member,
                                     category=Category.objects.get(title='sport_car'))

        self.selenium.find_element_by_link_text('پروفایل').click()
        self.selenium.find_element_by_link_text('آگهی‌های من').click()

    def test_create_ad(self):
        self.selenium.find_element_by_id('create_advertisement').click()

        title = self.selenium.find_element_by_id('title')
        select1 = Select(self.selenium.find_element_by_id("select1"))
        select2 = Select(self.selenium.find_element_by_id("select2"))
        category = Select(self.selenium.find_element_by_id("category"))

        state = Select(self.selenium.find_element_by_id("state"))
        city = Select(self.selenium.find_element_by_id("city"))
        desc = self.selenium.find_element_by_id('desc')
        price = self.selenium.find_element_by_id('price')

        submit = self.selenium.find_element_by_id('submit')

        title.send_keys('my ad')
        desc.send_keys('a good ad')
        price.send_keys(1000)

        select1.select_by_index(1)
        state.select_by_index(1)
        time.sleep(1)

        select2.select_by_index(1)
        city.select_by_index(1)
        time.sleep(1)

        category.select_by_index(1)

        submit.send_keys(Keys.RETURN)

        try:
            WebDriverWait(self.selenium, DELAY).until(EC.presence_of_element_located((By.TAG_NAME, 'img')))
        except TimeoutException:
            print('time out')

        assert 'my ad' in self.selenium.page_source

    def test_show_created_ad_in_my_ads(self):
        self.create_ad_and_move_to_my_ads()
        assert 'pride' in self.selenium.page_source

    def test_edit_ad(self):
        self.create_ad_and_move_to_my_ads()

        self.selenium.find_element_by_css_selector(
            '#page-content-wrapper > div > div.col-lg-4.mb-4 > div > div.card-footer > a.btn.btn-info').click()

        time.sleep(3)
        title = self.selenium.find_element_by_id('title')
        desc = self.selenium.find_element_by_id('desc')
        price = self.selenium.find_element_by_id('price')
        state = Select(self.selenium.find_element_by_id("state"))
        city = Select(self.selenium.find_element_by_id("city"))

        submit = self.selenium.find_element_by_id('submit')

        title.send_keys('edited title')
        desc.send_keys('a good edited ad')
        price.send_keys(1000)

        state.select_by_index(2)
        time.sleep(1)

        city.select_by_index(1)

        submit.send_keys(Keys.RETURN)

        try:
            WebDriverWait(self.selenium, DELAY).until(EC.presence_of_element_located((By.TAG_NAME, 'img')))
        except TimeoutException:
            print('time out')

        assert 'edited title' in self.selenium.page_source
        assert 'a good edited ad' in self.selenium.page_source

    def test_archive_ad(self):
        self.create_ad_and_move_to_my_ads()
        self.selenium.find_element_by_name('archive').click()
        time.sleep(1)
        self.selenium.find_element_by_css_selector('#myModal > div > div > div.modal-footer > form > button').click()
        self.selenium.find_element_by_link_text('دیوار').click()

        assert 'pride' not in self.selenium.page_source

    def test_bookmark(self):
        self.create_ad_and_move_to_my_ads()

        self.selenium.find_element_by_css_selector(
            '#page-content-wrapper > div:nth-child(1) > div:nth-child(1) > div > div.card-footer > a.btn.btn-primary').click()
        self.selenium.find_element_by_css_selector('#bookmark').click()

        self.selenium.find_element_by_link_text('پروفایل').click()
        self.selenium.find_element_by_link_text('آگهی‌های نشان‌شده').click()

        assert 'pride' in self.selenium.page_source

    def test_report_ad(self):
        self.create_ad_and_move_to_my_ads()

        self.selenium.find_element_by_css_selector(
            '#page-content-wrapper > div:nth-child(1) > div:nth-child(1) > div > div.card-footer > a.btn.btn-primary').click()
        report = self.selenium.find_element_by_css_selector('body > div:nth-child(2) > button')
        report.send_keys(Keys.RETURN)
        time.sleep(1)

        report = self.selenium.find_element_by_css_selector('#report-form > div > textarea')
        report.send_keys('inappropriate ad')
        submit = self.selenium.find_element_by_css_selector(
            '#myModal > div > div > div.modal-footer > button.btn.btn-success')
        submit.send_keys(Keys.RETURN)

        self.assertEqual(ReportAdvertisement.objects.all().first().reason, 'inappropriate ad')

    def test_ad_detail(self):
        Advertisement.objects.create(title='pride', price=500, is_urgent=True, description='good car',
                                     state='Tehran', city='Varamin', user=self.member,
                                     category=Category.objects.get(title='sport_car'))

        Advertisement.objects.create(title='peugeot', price=1000, is_urgent=True, description='good car',
                                     state='Tehran', city='Tehran', user=self.member,
                                     category=Category.objects.get(title='sport_car'))

        self.selenium.get(self.live_server_url)
        try:
            WebDriverWait(self.selenium, DELAY).until(EC.presence_of_element_located((By.TAG_NAME, 'img')))
        except TimeoutException:
            print('time out')

        self.selenium.find_element_by_css_selector(
            '#list_of_ads > div:nth-child(1) > div:nth-child(1) > div > div.card-footer > a').click()

        assert 'pride' in self.selenium.page_source
        assert '500' in self.selenium.page_source
        assert 'Tehran' in self.selenium.page_source
        assert 'Varamin' in self.selenium.page_source
        assert 'vehicle' in self.selenium.page_source
        assert 'car' in self.selenium.page_source
        assert 'sport_car' in self.selenium.page_source

        assert 'peugeot' in self.selenium.page_source  # relevant ad

    def test_show_agreement_in_ad_detail(self):
        Advertisement.objects.create(title='agreement ad', price=-1, is_urgent=True, description='good car',
                                     state='Tehran', city='Tehran', user=self.member,
                                     category=Category.objects.get(
                                         title='sport_car'))  # the -1 price indicated agreement

        self.selenium.get(self.live_server_url)
        try:
            WebDriverWait(self.selenium, DELAY).until(EC.presence_of_element_located((By.TAG_NAME, 'img')))
        except TimeoutException:
            print('time out')

        self.selenium.find_element_by_css_selector(
            '#list_of_ads > div:nth-child(1) > div:nth-child(1) > div > div.card-footer > a').click()

        assert 'توافقی' in self.selenium.page_source
