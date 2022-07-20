from django.core import mail
from django.http.request import HttpRequest
from django.test.utils import override_settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator

from rest_framework.test import APITestCase

from users.serializers import ( ActivateInvitedUserSerializer, ContactUsSerializer, UserInvitationSerializer, 
    UserSerializer, UserUpdateSerializer, ResetPasswordConfirmSerializer, ValidateTokenSerializer, 
    ChangePasswordSerializer )
from users.tests.factories import UserFactory
from accounts.tests.factories import AccountFactory


class UserSerializerTest(APITestCase):

    def test_user_serializer(self):
        '''Test user serializer :is_valid() and :create() methods'''

        # create incomplete data
        data = {
            'email': 'miracle@example.com',
            'password': 'example',
        }
        invalid_serializer = UserSerializer(data=data)

        # assert serilizer data checks validity
        self.assertFalse(invalid_serializer.is_valid())

   
        valid_serializer = UserSerializer(data=data)

        self.assertTrue(valid_serializer.is_valid())

        # assert a user is returned when :create() method is called
        user = valid_serializer.create(valid_serializer.validated_data)
        self.assertEqual(user.email, data['email'])






class ResetPasswordSerializerTest(APITestCase):
    
    def test_token_validation(self):
        '''Assert that token validation works as expected for the reset password 
        serializers - :is_valid() and :validate_token() methods
        '''

        # create data
        user = UserFactory()
        token = default_token_generator.make_token(user)
        uid =  urlsafe_base64_encode(force_bytes(user.id))
        data = {
            'uid': uid,
            'token': token,
        }
        # check validity of both serializers
        invalid_rpc_serializer = ResetPasswordConfirmSerializer(data=data)
        valid_vt_serializer = ValidateTokenSerializer(data=data)
        self.assertFalse(invalid_rpc_serializer.is_valid())
        self.assertTrue(valid_vt_serializer.is_valid())

        # update data for invalid serializer 
        data['password'] = '@thiscool123'

        # Assert serializer is now valid and reset password
        valid_rpc_serializer = ResetPasswordConfirmSerializer(data=data)
        self.assertTrue(valid_rpc_serializer.is_valid())
        valid_rpc_serializer.reset_password()

        # Assert password has been changed
        self.assertNotEqual(valid_rpc_serializer.user.password, user.password)





