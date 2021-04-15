#-----------------------------------------------------------------------------
# frontend.py
# 
# Frontend common methods
#-----------------------------------------------------------------------------

import sys
sys.path.insert(0, '..')
from test_app import create_app

from flask_testing import LiveServerTestCase
from selenium.webdriver.firefox.options import Options  
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium import webdriver

import unittest

SERVER_URL = 'http://localhost:3000'

SCHEDULE_HELP = 'https://docs.google.com/document/d/1FZGoeQps5YBUeevAp_zUig0guIGgJjFvd-dx14NKvZY/edit?usp=sharing'
HOST_HELP = 'https://docs.google.com/document/d/1uFg-jsFCzDis5LvxQ1Kj1aIRS7ndyUPSUJRlZSwnoBI/edit?usp=sharing'

class TestBase(unittest.TestCase):
    
    url = SERVER_URL

    def setUp(self):
        options = Options()
        options.add_argument('--headless')

        self.driver =  webdriver.Firefox(options=options,
                                         executable_path='C:\geckodriver.exe')
        self.driver.get(self.url)
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()

    def header_test(self, logged_in=False, check_button=True):
        brand = self.driver.find_element_by_class_name('navbar-brand')

        # check image
        img = brand.find_element_by_tag_name('img')
        self.assertEqual(img.get_attribute('src'),
                         SERVER_URL + '/static/react/images/favicon.ico')
        self.assertEqual(img.get_attribute('alt'), 'Clock Favicon')

        # check text
        self.assertEqual(brand.text, 'Docketer')

        if check_button:
            # check login button (not logged in)
            button = self.driver.find_element_by_id('login-button')
            self.assertEqual(button.get_attribute('innerHTML'), 
                            'Login' if not logged_in else 'Logout')

    def footer_test(self, URL=HOST_HELP):
        footer = self.driver.find_element_by_tag_name('footer')
        self.assertEqual(footer.text,
            'Created for Junior IW (Spring 2021) by Erin Vuong. For help click here.')

        link = footer.find_element_by_tag_name('a')
        self.assertEqual(link.get_attribute('href'), URL)

    def check_simple_form_group(self, 
                                form_group,
                                label,
                                info,
                                value=None,
                                placeholder=None,
                                textarea=False):
        label_comp = form_group.find_element_by_tag_name('label')
        self.assertEqual(label_comp.text, label)

        tag = 'input'
        if textarea:
            tag = 'textarea'
        input = form_group.find_element_by_tag_name(tag)
        self.assertEqual(input.get_attribute('info'), info)
        if value is not None:
            self.assertEqual(input.get_attribute('value'), value)
        if placeholder is not None:
            self.assertEqual(input.get_attribute('placeholder'), placeholder)

if __name__ == '__main__':
    unittest.main()