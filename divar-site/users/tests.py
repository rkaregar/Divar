from django.test import TestCase
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.keys import Keys
from users.models import Member
from django.contrib.auth.models import User

import time


def create_member(username='test', password='test'):
    user = User.objects.create_user(username=username, password=password)
    member = Member.objects.create(user=user, phone_number='123456')

    return member


def login(selenium, live_server_url, input_username, input_password):
    selenium.get(live_server_url + '/users/login/')

    username = selenium.find_element_by_id('username')
    password = selenium.find_element_by_id('password')

    submit = selenium.find_element_by_id('submit_button')

    username.send_keys(input_username)
    password.send_keys(input_password)

    submit.send_keys(Keys.RETURN)


class UserTest(StaticLiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Chrome()
        super(UserTest, self).setUp()

        self.member = create_member('test', 'test')

    def tearDown(self):
        self.selenium.quit()
        super(UserTest, self).tearDown()

    def test_login_wrong_username_password(self):
        login(self.selenium, self.live_server_url, 'test', 'wrong')

        assert "Please enter a correct username and password" in self.selenium.page_source

        login(self.selenium, self.live_server_url, 'wrong', 'test')

        assert "Please enter a correct username and password" in self.selenium.page_source

        login(self.selenium, self.live_server_url, 'test', 'test')

        time.sleep(1)
        assert 'آگهی‌ای پیدا نشد' in self.selenium.page_source

    def test_change_password(self):
        login(self.selenium, self.live_server_url, 'test', 'test')

        self.selenium.find_element_by_link_text('پروفایل').click()
        self.selenium.find_element_by_link_text('تغییر رمز عبور').click()

        old_password = self.selenium.find_element_by_id('old_password')
        new_password = self.selenium.find_element_by_id('new_password')
        new_password_confirmation = self.selenium.find_element_by_id('new_password_confirmation')

        submit_button = self.selenium.find_element_by_id('submit_button')

        old_password.send_keys('test')
        new_password.send_keys('IHaveChosenANewPasswordForMyAccount')
        new_password_confirmation.send_keys('IHaveChosenANewPasswordForMyAccount')

        submit_button.send_keys(Keys.RETURN)

        assert 'رمز عبور شما با موفقیت تغییر کرد' in self.selenium.page_source

        self.selenium.find_element_by_link_text('خروج').click()

        login(self.selenium, self.live_server_url, 'test', 'test')
        assert "Please enter a correct username and password" in self.selenium.page_source

        login(self.selenium, self.live_server_url, 'test', 'IHaveChosenANewPasswordForMyAccount')
        time.sleep(1)

        assert 'آگهی‌ای پیدا نشد' in self.selenium.page_source

    def test_change_phone_number(self):
        login(self.selenium, self.live_server_url, 'test', 'test')

        self.selenium.find_element_by_link_text('پروفایل').click()
        self.selenium.find_element_by_link_text('تغییر شماره تلفن').click()

        phone_number = self.selenium.find_element_by_id('phone_number')
        submit_button = self.selenium.find_element_by_id('submit_button')

        phone_number.send_keys('123456789012345')
        submit_button.send_keys(Keys.RETURN)

        assert "Phone number: Ensure this value has at most 12 characters" in self.selenium.page_source

        phone_number = self.selenium.find_element_by_id('phone_number')
        submit_button = self.selenium.find_element_by_id('submit_button')

        phone_number.clear()
        phone_number.send_keys('123456789')
        submit_button.send_keys(Keys.RETURN)

        time.sleep(1)
        assert 'آگهی‌ای پیدا نشد' in self.selenium.page_source

        self.selenium.find_element_by_link_text('پروفایل').click()
        self.selenium.find_element_by_link_text('تغییر شماره تلفن').click()

        assert '123456789' in self.selenium.page_source


