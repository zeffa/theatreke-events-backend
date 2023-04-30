import string

import requests

from main.settings import MPESA_CONSUMER_KEY, MPESA_CONSUMER_SECRET, MPESA_BASE_URL, PASS_KEY, SHORT_CODE
from mpesa.helpers import basic_authorization, auth_response, get_password, get_timestamp


class LipaNaMpesa:
    def __init__(self):
        self.shortcode = SHORT_CODE

    def get_access_token(self) -> string:
        try:
            authorization = basic_authorization(MPESA_CONSUMER_KEY, MPESA_CONSUMER_SECRET)
            response = auth_response(authorization, MPESA_BASE_URL, requests).json()
            return response['access_token']
        except KeyError:
            return ""

    def stk_push(self, phone_number, amount):
        timestamp = get_timestamp()
        token = self.get_access_token()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer %s" % token
        }
        url = '%s/mpesa/stkpush/v1/processrequest' % MPESA_BASE_URL
        password = get_password(self.shortcode, PASS_KEY, timestamp)
        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": "%s" % timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": "https://api.kenyatheatreawards.com/api/v1/awards/payments/transactions",
            "AccountReference": "Mofit Kochez %s" % self.shortcode,  # Company Account Number
            "TransactionDesc": "Payment of Kochez Services"
        }
        response = requests.request("POST", url=url, headers=headers, json=payload)
        return response

    def c2b_checkout(self):
        pass

    def register_callbacks(self):
        url = "%s/mpesa/c2b/v1/registerurl" % MPESA_BASE_URL
        token = self.get_access_token()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer %s" % token
        }
        payload = {
            "ShortCode": self.shortcode,
            "ResponseType": "Completed",
            "ConfirmationURL": "https://api.kenyatheatreawards.com/api/v1/awards/payments/transactions",
            "ValidationURL": "https://api.kenyatheatreawards.com/api/v1/awards/payments/transactions"
        }
        response = requests.request("POST", url=url, headers=headers, json=payload)
        return response
