# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
class LogInTest(TestCase):
    
    
    def test_login_use_empty_username_password(self):
        print '******************test_login_use_empty_username_password()**********************'
        login_account_test_data = {'username':'', 'password':''}
        # send POST request.
        response = self.client.post(path='/login/', data=login_account_test_data)
        print 'Response status code : ' + str(response.status_code)
        #print('Response content : ' + str(response.content))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('User name can not be empty.', response.content)
        self.assertIn(u'Password can not be empty.', response.content)
    
    def test_login_username_or_password_not_correct(self):
        print '******************test_login_username_or_password_not_correct()**********************'
        login_account_test_data = {'username': 'admin', 'password': 'asas'}
        response = self.client.post(path='/login/', data=login_account_test_data)
        print 'Response status code : ' + str(response.status_code)
        #print('Response content : ' + str(response.content))
        self.assertEqual(response.status_code, 200)
        # if the provided string exist in the response content html, then pass.
        self.assertIn(u'User name or password is not correct.', response.content)
    
    def test_login_success(self):
        print '******************test_login_success()**********************'
        login_account_test_data = {'username': 'admin', 'password': 'battlehome'}
        response = self.client.post(path='/login/', data=login_account_test_data)
        print 'Response status code : ' + str(response.status_code)
        self.assertNotIn(u'User name or password is not correct', response.content)

    def test_home_page(self):
        print '******************test_home_page()**********************'
        # send GET request.
        response = self.client.get('/')
        print 'Response status code : ' + str(response.status_code)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')