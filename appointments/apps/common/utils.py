from django.conf import settings

from itsdangerous import URLSafeSerializer

def get_serializer(secret_key=None):
    if secret_key is None:
        secret_key = settings.config['SECRET_KEY']
    return URLSafeSerializer(secret_key)