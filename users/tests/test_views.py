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
        self.assertEqual(resp.data['message'], 'Invalid credentials')

    def test_incomplete_credentials(self):
        '''Login with incomplete credentials'''

        data = { 
            'email': 'miracle@mysite.com'
        }
        resp = self.client.post(self.url, data=data)
    
        self.assertEqual(resp.status_code, 400)


    def test_login(self):
        '''Login with correct credentials'''

        # set up data
        user = UserFactory(**self.auth_data, email_verified=True)
       
        login = self.client.post(self.url, data=self.auth_data)
       
        self.assertEqual(login.status_code, 200)
        self.assertEqual(login.data['message'], 'Login successful')
        self.client.logout()


class SignUpViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):

        cls.url = '/users/signup/'
        cls.data = {
                    'password':'@thiscool123',
                    'email':'email@example.com',
                    'phone': '081111111111',
                    'first_name': 'miracle',
                    'last_name': 'alex'
                    }

    def test_user_creation(self):
        '''Test create new user '''

        resp = self.client.post(self.url, self.data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn('User created', resp.data['message'])
        self.assertEqual(resp.data['data']['email'], self.data['email'])



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
        self.assertEqual(resp.data['message'], 'Token is valid')

    def test_password_reset_confirm(self):
        '''Assert that reset was confirmed'''

        # create a user and tokens
        user = UserFactory(email="email@gmail.com")
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        token = default_token_generator.make_token(user)

        # Assert password is reset
        pwd_reset_confirm_url = '/users/reset-password-confirm/'
        pwd_reset_confirm_data = {
            'uid': uidb64, 'token': token, 'password': 'mysite123445'
        }
        resp = self.client.post(pwd_reset_confirm_url, pwd_reset_confirm_data)
        
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['message'], 'Password reset was successful')

