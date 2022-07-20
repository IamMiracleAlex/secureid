from django.test import SimpleTestCase
from django.urls import resolve

from users import views


class UserUrlsResolvesToViewTest(SimpleTestCase):

    def test_login_url_resolves_to_login_view(self):
        '''assert that login url resolves to the login view class'''

        found = resolve('/users/login/')
        # use func.view_class to get the class for the view
        self.assertEqual(found.func.view_class, views.LoginView)

    
    def test_signup_url_resolves_to_register_view(self):
        '''assert that the signup url resolves to the register view'''

        found = resolve('/users/signup/')
        self.assertEqual(found.func.view_class, views.SignUpView)       
      
    
    def test_user_detail_update_url_resolves_to_detail_view(self):
        '''assert that the user me url resolves to the user detail & update view'''

        found = resolve('/users/me/')
        self.assertEqual(found.func.view_class, views.UserDetailUpdateView)         

    
    def test_password_reset_request_url_resolves_to_view(self):
        '''assert that the password reset request url resolves to the right view'''

        found = resolve('/users/password-reset-request/')
        self.assertEqual(found.func.view_class, views.ResetPasswordRequest)         
      
    def test_reset_password_validate_token_url_resolves_to_view(self):
        '''assert that the reset password validate token url resolves to the correct view'''

        found = resolve('/users/reset-password-validate-token/')
        self.assertEqual(found.func.view_class, views.ResetPasswordValidateToken)         
      
      
    def test_reset_password_confirm_url_resolves_to_view(self):
        '''assert that the reset password confirm url resolves to the correct view'''

        found = resolve('/users/reset-password-confirm/')
        self.assertEqual(found.func.view_class, views.ResetPasswordConfirm)         
      
      
   
