from django.contrib.auth import authenticate, login
from django.contrib.auth.signals import user_logged_in

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


from helpers.utils import send_password_reset_mail
from helpers.api_response import SuccessResponse, FailureResponse
from helpers.utils import  jwt_token
from users import serializers as ser
from users.models import  User
from users.signals import reset_password_token_created

class LoginView(APIView):
    '''
    Login users
    POST /users/login/
    '''
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=ser.UserLoginSerializer, responses={200: ser.UserSerializer} )
    def post(self, request):
        
        serializer = ser.UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")

        user = authenticate(email=email, password=password)
        if not user:
            return FailureResponse(
				message='Invalid credentials',
				status=status.HTTP_401_UNAUTHORIZED
            )

        login(request, user)

        user_logged_in.send(sender=request.user.__class__,
            request=request, user=request.user)    
        data = ser.UserSerializer(user, context={'request': request}).data
        
        data['token'] = jwt_token(user)

        return SuccessResponse(message='Login successful', data=data)



class SignUpView(APIView):
    '''
    Create new user accounts
    POST /users/signup/
    '''
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=ser.UserSerializer, responses={201: ser.UserSerializer} )
    def post(self, request):
        serializer = ser.UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
                 
        return SuccessResponse(
                message='User created successfully',
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
				

class ResetPasswordRequest(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=ser.ResetPasswordRequestSerializer)
    def post(self, request, *args, **kwargs):
        """
        An api view which provides a method to request a password reset token based on an e-mail address
        Sends a signal reset_password_token_created when a reset token was created.
        POST /users/password-reset-request/
        """

        serializer = ser.ResetPasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
     
        # find a user by email address (case insensitive search)
        user = User.objects.filter(email__iexact=email)

        if user.exists() and getattr(user.first(), 'is_active', False):
            send_password_reset_mail(user.first())            
            # send a signal that the password token was created
            reset_password_token_created.send(sender=self.__class__, user=user.first())
        return SuccessResponse(message='Kindly check your email to set your password')


class ResetPasswordValidateToken(APIView):
    """
    An api view which provides a method to verify that a token is valid
    POST /users/reset-password-validate-token/
    """
    permission_classes = [AllowAny]
    serializer_class = ser.ValidateTokenSerializer

    @swagger_auto_schema(request_body=ser.ValidateTokenSerializer )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return SuccessResponse(message="Token is valid")


class ResetPasswordConfirm(APIView):
    """
    An Api View which provides a method to reset a password based on a unique token
    POST /users/reset-password-confirm/
    """
    permission_classes = [AllowAny]
    serializer_class = ser.ResetPasswordConfirmSerializer

    @swagger_auto_schema(request_body=ser.ResetPasswordConfirmSerializer )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.reset_password()
        return SuccessResponse(message="Password reset was successful")

    

class HomeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = {
            "service": "Secure ID API",
            "version": "1.0"
        }
        message = "Welcome to secure ID"
        return SuccessResponse(message=message, data=data)

