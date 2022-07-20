from django.contrib.auth.password_validation import validate_password, get_password_validators
from django.conf import settings


from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User
from users.signals import pre_password_reset, post_password_reset
from helpers.utils import validate_token



class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,
                validators=[UniqueValidator(queryset=User.objects.all(),
                message='User with this email already exists', lookup='iexact')])
    password = serializers.CharField(min_length=8, write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone = serializers.CharField()


    def validate_password(self, value):
        try:
            validate_password(
                password=value,
                password_validators=get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)
            )
            return value
        except Exception as e:
            raise serializers.ValidationError(e) 

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name','full_name','phone', ]

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user

class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class TokenValidateMixin:
    def validate(self, data):
        token = data.get('token')
        uid = data.get('uid')

        user, is_valid = validate_token(uid, token)
        if not (user and is_valid):
            raise serializers.ValidationError("The token entered is not valid. Please check and try again.")
        self.user = user

        password = data.get('password')
        if password:
            try:
                validate_password(
                    password=password,
                    user=self.user,
                    password_validators=get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)
                )
            except Exception as e:
                raise serializers.ValidationError(e)
        return data


class ResetPasswordConfirmSerializer(TokenValidateMixin, serializers.Serializer):
    password = serializers.CharField()
    token = serializers.CharField()
    uid = serializers.CharField()

    def reset_password(self):
        password = self.validated_data.get('password')
        
        pre_password_reset.send(sender=self.__class__, user=self.user)
    
        self.user.set_password(password)
        self.user.save()

        post_password_reset.send(sender=self.__class__, user=self.user)

        return


class ValidateTokenSerializer(TokenValidateMixin, serializers.Serializer):
    token = serializers.CharField()
    uid = serializers.CharField()



    

