from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator  
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from rest_framework_jwt.settings import api_settings

from users.models import User




def validate_token(uidb64, token):
    is_valid = False

    try:
        id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        is_valid = True
    
    return user, is_valid


def jwt_token(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token


def send_password_reset_mail(user):
	context = {
		'name': user.first_name,
		'uid': urlsafe_base64_encode(force_bytes(user.id)),
		'token': default_token_generator.make_token(user),
	}
	email = user.email
	message = render_to_string('users/password_reset.txt', context)
	subject = 'Reset Your Password'
	send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
