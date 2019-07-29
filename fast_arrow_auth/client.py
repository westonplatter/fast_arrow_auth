import json
import os
import uuid

import requests

from fast_arrow_auth.util import get_last_path
from fast_arrow_auth.resources.account import Account
from fast_arrow_auth.exceptions import AuthenticationError
from fast_arrow_auth.exceptions import NotImplementedError

CLIENT_ID = "c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS"

HTTP_ATTEMPTS_MAX = 2


class Client(object):
    def __init__(self, **kwargs):
        self.options = kwargs
        self.device_token = self.options.get("device_token")
        self.account_id = None
        self.account_url = None
        self.access_token = None
        self.token_type = None
        self.refresh_token = None
        self.mfa_code = self.options.get("mfa_code")
        self.scope = None
        self.authenticated = False
        self.certs = os.path.join(
            os.path.dirname(__file__), 'ssl_certs/certs.pem')

    def gen_credentials(self):
        return {
            "account_id": self.account_id,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "scope": self.scope,
            "token_type": self.token_type,
            "device_token": self.device_token,
        }

    def write_credentials_to_file(self, filename):
        creds = self.gen_credentials()
        with open(filename, "w") as f:
            f.write(json.dumps(creds, indent=4))

    def authenticate(self):
        '''
        Authenticate using data in `options`
        '''
        if "username" in self.options and "password" in self.options:
            kwargs = {
                "mfa_code": self.mfa_code,
                "device_token": self.device_token,
            }

            self.login_oauth2(
                self.options["username"],
                self.options["password"],
                kwargs)

        elif "access_token" in self.options:
            if "refresh_token" in self.options:
                self.access_token = self.options["access_token"]
                self.refresh_token = self.options["refresh_token"]
                self.__set_account_info()
        else:
            self.authenticated = False
        return self.authenticated

    def get(self, url, params=None):
        '''
        Execute HTTP GET
        '''
        headers = self._gen_headers(self.access_token, url)
        res = requests.get(url, headers=headers)
        return res.json()

    def post(self, url, payload=None, extra_headers={}):
        '''
        Execute HTTP POST
        '''
        default_headers = self._gen_headers(self.access_token, url)
        headers = {**default_headers, **extra_headers}
        res = requests.post(url,
                            headers=headers,
                            data=json.dumps(payload),
                            timeout=15,
                            verify=self.certs)
        if res.headers['Content-Length'] == '0':
            return None
        else:
            return res.json()

    def _gen_headers(self, bearer, url):
        '''
        Generate headders, adding in Oauth2 bearer token if present
        '''
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": ("en;q=1, fr;q=0.9, de;q=0.8, ja;q=0.7, " +
                                "nl;q=0.6, it;q=0.5"),
            "Content-Type": "application/json",
            "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) " +
                           "AppleWebKit/537.36 (KHTML, like Gecko) " +
                           "Chrome/68.0.3440.106 Safari/537.36"),
        }
        if bearer:
            headers["Authorization"] = "Bearer {}".format(bearer)
        if url == 'https://api.robinhood.com/user/':
            del headers["Content-Type"]
        return headers

    def login_oauth2(self, username, password, kwargs):
        '''
        Login using username and password
        '''

        if kwargs["device_token"]:
            device_token = kwargs["device_token"]
        else:
            device_token = str(uuid.uuid4())

        if "challenge_type" in kwargs:
            challenge_type = kwargs["challenge_type"]
        else:
            challenge_type = "sms"

        data = {
            "client_id": CLIENT_ID,
            "device_token": device_token,
            "expires_in": 86400,
            "grant_type": "password",
            "password": password,
            "scope": "internal",
            "username": username,
            "challenge_type": challenge_type
        }

        if kwargs["mfa_code"]:
            mfa_code = kwargs["mfa_code"]
            data["mfa_code"] = mfa_code

        url = "https://api.robinhood.com/oauth2/token/"

        res = self.post(url, payload=data)

        if "detail" in res:
            challenge_started_text = "Request blocked, challenge issued."
            if res["detail"] == challenge_started_text:
                challenge = res["challenge"]
                challenge_url = (
                    "https://api.robinhood.com/challenge/{}/respond/"
                    .format(challenge["id"]))

                print("Input challenge code from '{}'".format(challenge_type))
                user_input_response_code = input()

                body = {"response": str(user_input_response_code)}
                data_challenge = self.post(challenge_url, body)
                if data_challenge["status"] == "validated":
                    challenge_id = data_challenge["id"]
                else:
                    print("challenge response was not accepted")

                extra_headers = {
                    "X-ROBINHOOD-CHALLENGE-RESPONSE-ID": challenge_id
                }

                res = self.post(url, payload=data, extra_headers=extra_headers)

                self.token_type = res["token_type"]
                self.access_token = res["access_token"]
                self.refresh_token = res["refresh_token"]
                self.mfa_code = res["mfa_code"]
                self.scope = res["scope"]
                self.__set_account_info()
                self.write_credentials_to_file("fast_arrow_auth.json")
                return self.authenticated

        else:
            self.token_type = res["token_type"]
            self.access_token = res["access_token"]
            self.refresh_token = res["refresh_token"]
            self.mfa_code = res["mfa_code"]
            self.scope = res["scope"]
            self.__set_account_info()
            self.write_credentials_to_file("fast_arrow_auth.json")
            return self.authenticated

    def __set_account_info(self):
        account_urls = Account.all_urls(self)
        if len(account_urls) > 1:
            msg = ("fast_arrow 'currently' does not handle " +
                   "multiple account authentication.")
            raise NotImplementedError(msg)
        elif len(account_urls) == 0:
            msg = "fast_arrow expected at least 1 account."
            raise AuthenticationError(msg)
        else:
            self.account_url = account_urls[0]
            self.account_id = get_last_path(self.account_url)
            self.authenticated = True

    def relogin_oauth2(self):
        '''
        (Re)login using the Oauth2 refresh token
        '''
        url = "https://api.robinhood.com/oauth2/token/"
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "scope": "internal",
            "client_id": CLIENT_ID,
            "expires_in": 86400,
        }
        res = self.post(url, payload=data)
        self.access_token = res["access_token"]
        self.refresh_token = res["refresh_token"]
        self.mfa_code = res["mfa_code"]
        self.scope = res["scope"]
        return True

    def logout_oauth2(self):
        '''
        Logout for given Oauth2 bearer token
        '''
        url = "https://api.robinhood.com/oauth2/revoke_token/"
        data = {
            "client_id": CLIENT_ID,
            "token": self.refresh_token,
        }
        res = self.post(url, payload=data)
        if res is None or res == {}:
            self.account_id = None
            self.account_url = None
            self.access_token = None
            self.refresh_token = None
            self.mfa_code = None
            self.scope = None
            self.authenticated = False
            return True
        else:
            raise AuthenticationError("fast_arrow could not log out.")
