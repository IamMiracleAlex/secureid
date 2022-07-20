from unittest import skip

from django.utils import timezone
from django.core import mail
from django.test.utils import override_settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from rest_framework import status
from rest_framework.test import APITestCase

from users.tests.factories import  UserFactory


class LoginViewTest(APITestCase):   

    @classmethod
    def setUpTestData(cls):
        cls.auth_data = { 
            'password': '@thiscool123',
            'email': 'miracle@mysite.com'
        }     
        cls.url = '/users/login/'

    def test_invalid_user(self):
        '''login with invalid credentials'''

        data = { 
            'email': 'email@gmail.com',
            'password': '@thiscool123'
        }
        resp = self.client.post(self.url, data)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(resp.data['detail'], 'Invalid credentials')

    def test_incomplete_credentials(self):
        '''Login with incomplete credentials'''

        data = { 
            'email': 'miracle@mysite.com'
        }
        resp = self.client.post(self.url, data=data)
    
        self.assertEqual(resp.status_code, 400)

    def test_unverified_email(self):
        '''Assert user can't login with unverified email'''
        UserFactory(**self.auth_data)

        login = self.client.post(self.url, data=self.auth_data)
        self.assertEqual(login.status_code, 403)
        self.assertEqual(login.data['detail'], 'Please verify your email address')
       
    def test_login(self):
        '''Login with correct credentials'''

        # set up data
        user = UserFactory(**self.auth_data, email_verified=True)
       
        login = self.client.post(self.url, data=self.auth_data)
       
        self.assertEqual(login.status_code, 200)
        self.assertEqual(login.data['detail'], 'Login successful')
        self.client.logout()


class SignUpViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):

        cls.url = '/users/signup/'
        cls.data = {
                    'password':'@thiscool123',
                    'email':'email@example.com',
                    'account_name': 'mysite',
                    'account_type': 'Individual',
                    'currency': 'NGN'
                    }

    def test_user_creation(self):
        '''Test create new user '''

        resp = self.client.post(self.url, self.data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn('User created', resp.data['detail'])
        self.assertEqual(resp.data['data']['email'], self.data['email'])


class UserDetailUpdateViewTest(APITestCase):

    def setUp(self):

        self.detail_url = '/users/me/'
        self.user = UserFactory()

    def test_user_details_get_method(self):
        '''Assert that get method for user details works. user is retrieved by their token'''
         
        self.client.force_authenticate(self.user)       
        resp = self.client.get(self.detail_url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['data']['phone'], self.user.phone)

    def test_user_detail_put_method(self):
        '''Assert that put method for user details works. Data is sent to the user using their token'''

        new_data = {'first_name':'Miracle', 
                    'last_name':'Alex',
                    'email': 'example@gmail.com'} 

        # update data and assert they were updated
        self.client.force_authenticate(self.user)       
        resp = self.client.put(self.detail_url, new_data) 

        self.assertEqual(resp.data['data']['phone'], self.user.phone)
        self.assertEqual(resp.data['data']['first_name'], new_data['first_name'])
        self.assertEqual(resp.data['data']['last_name'], new_data['last_name'])




class PasswordResetTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_password_reset_request(self):
        '''Assert that password reset token was sent'''

        pwd_req_url = '/users/password-reset-request/'
        resp = self.client.post(pwd_req_url, {'email': self.user.email})

        # assert request is successfull and mail was sent
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)

    def test_validate_token(self):
        '''Assert that token is valid'''

        # create a user and tokens
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.id))
        token = default_token_generator.make_token(self.user)

        # test validate token url
        validate_token_url = '/users/reset-password-validate-token/'
        validate_token_data = {'uid': uidb64, 'token': token}
        resp = self.client.post(validate_token_url, validate_token_data)

        # Assert validate token is  successful
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['detail'], 'Token is valid')

    def test_password_reset_confirm(self):
        '''Assert that reset was confirmed'''

        # create a user and tokens
        user = UserFactory(email="email@gmail.com")
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        token = default_token_generator.make_token(user)

        # Assert password is reset
        pwd_reset_confirm_url = '/users/reset-password-confirm/'
        pwd_reset_confirm_data = {
            'uid': uidb64, 'token': token, 'password': 'mysite'
        }
        resp = self.client.post(pwd_reset_confirm_url, pwd_reset_confirm_data)
        
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['detail'], 'Password reset was successful')

