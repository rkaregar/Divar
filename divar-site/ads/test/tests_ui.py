from django.test import LiveServerTestCase
from selenium import webdriver
from ads.test.tests_models import create_member, create_categories
import time


class SearchTest(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Chrome()

        super(SearchTest, self).setUp()

        create_categories()
        self.member = create_member('test', 'test')

    def tearDown(self):
        self.selenium.quit()
        super(SearchTest, self).tearDown()

    def test_redirect_to_homepage(self):
        selenium = self.selenium
        selenium.get(self.live_server_url)

        self.assertEqual(selenium.current_url, self.live_server_url + '/ads/')


