from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator  

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


