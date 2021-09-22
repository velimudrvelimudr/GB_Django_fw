from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from requests import api
from social_core.exceptions import AuthForbidden

from auth_app.models import BookUserProfile

def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse((
        'https',
        'api.vk.com',
        '/method/user.get',
        None,
        urlencode(OrderedDict(
            fields=','.join(('bdate', 'sex', 'about')),
            access_token=response['access_token'],
            v='5.131'
        )),
        None
    ))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]
    if data['sex']:
        user.bookuserprofile.gender = BookUserProfile.MALE if data['sex'] == 2 else BookUserProfile.FEMALE

    if data['about']:
        user.bookuserprofile.aboutme = data['about']

    if data['bdate']:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

        age = timezone.now().date().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    user.save()

