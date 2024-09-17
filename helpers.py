import string
import random
import api


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string


def generate_random_email(length):
    login = generate_random_string(length)
    return login + '@yandex.ru'


def generate_random_field(field, length):
    if field == 'email':
        return generate_random_email(length)
    else:
        return generate_random_string(length)


def generate_new_user_credentials(empty_field=None):
    email = generate_random_email(10)
    password = generate_random_string(10)
    name = generate_random_string(10)

    credentials = {
        "email": email,
        "password": password,
        "name": name
    }
    if empty_field is not None:
        credentials[empty_field] = ""
    return credentials


def login_user(credentials):
    new_credentials = {
        'email': credentials['email'],
        'password': credentials['password']
    }
    response = api.login_user(new_credentials)
    response_payload = response.json()
    credentials['accessToken'] = response_payload['accessToken']


def create_user(credentials, login=False):
    response = api.create_user(credentials)
    response_payload = response.json()
    credentials['accessToken'] = response_payload['accessToken']

    if login:
        login_user(credentials)
    return credentials

def delete_user(credentials):
    api.delete_user(credentials['accessToken'])

def try_to_delete_user(credentials):
    response = api.login_user(credentials)
    if response.status_code == 200 and 'accessToken' in response.json():
        api.delete_user(response.json()['accessToken'])

def get_available_ingredient_hashes(limit=2):
    response = api.get_ingredients()
    objects = response.json()['data']

    hashes = []
    for obj in objects:
        hashes.append(obj['_id'])
        if len(hashes) >= limit:
            break
    return hashes