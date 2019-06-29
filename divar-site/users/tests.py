from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from users.models import Member
from django.contrib.auth.models import User


def create_member(username, password):
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