import base64
import string

import phonenumbers
from phonenumbers import PhoneNumberFormat


def basic_authorization(consumer_key, consumer_secret):
    string_to_encode = "%s:%s" % (consumer_key, consumer_secret)
    encoded_string = base64.b64encode(string_to_encode.encode('utf-8'))
    return encoded_string.decode('utf-8')


def get_password(short_code, pass_key, timestamp):
    string_to_encode = "%s%s%s" % (short_code, pass_key, timestamp)
    encoded_string = base64.b64encode(string_to_encode.encode('utf-8'))
    return encoded_string.decode('utf-8')


def auth_response(authorization, base_url, requests):
    headers = {'Authorization': "Basic %s" % authorization}
    url = "%s/oauth/v1/generate?grant_type=client_credentials" % base_url
    return requests.request("GET", url=url, headers=headers)


def get_timestamp():
    from datetime import datetime
    now = datetime.now()
    return now.strftime("%Y%m%d%H%M%S")


def format_phone_number(phone_number) -> string:
    parsed_phone_number = phonenumbers.parse(phone_number, region='KE')
    formatted_phone_number = phonenumbers.format_number(parsed_phone_number, PhoneNumberFormat.E164)[1:]
    return formatted_phone_number


def write_json_to_file(json, data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

