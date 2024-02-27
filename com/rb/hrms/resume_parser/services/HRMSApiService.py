import json

import requests
from com.rb.hrms.resume_parser.constants.HRMSApiConstants import *
from com.rb.hrms.resume_parser.utils.ConvertNullToNone import ConvertNullToNone


class HRMSApiService:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.jwt_token = None
        self.headers = None

    def form_headers(self):
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': "*/*",
            'X-TenantID': "redberyltech"
        }
        if self.jwt_token:
            self.headers['Authorization'] = f'Bearer {self.jwt_token}'
        # self.hrms_headers = self.headers
        return self.headers


    def get_headers(self):
        return self.headers

    def login(self):
        login_url = f'{self.base_url}/api/user/signin'
        credentials = {
            "username": self.username,
            "password": self.password
        }
        response = requests.post(login_url, json=credentials, headers=self.form_headers())

        if response.status_code == 201:
            self.jwt_token = response.json().get('accessToken')
            # self.form_headers()
            self.headers['Authorization'] = f'Bearer {self.jwt_token}'
            print("Login Successful. JWT Token obtained.")
        else:
            print(f"Login Failed. Status Code: {response.status_code}, Message: {response.text}")

    def logout(self):
        logout_url = f'{self.base_url}/api/user/logout'  # Update with the actual logout endpoint
        response = requests.post(logout_url, headers=self.get_headers())

        if response.status_code == 200:
            print("Logout Successful.")
        else:
            print(f"Logout Failed. Status Code: {response.status_code}, Message: {response.text}")

    def hrms_api_call(self, headers, method, url, data=None):
        try:

            print(type(data))
            json_data = json.dumps(data)
            response = requests.request(headers=headers, method=method, data=json_data, url=url)
            response.raise_for_status()
            print(response.json())
            if response:
                print(f"API Call to {url} | Method: {method} | Status Code: {response.status_code}")
                return response.json() if 'application/json' in response.headers.get('Content-Type',
                                                                                     '') else response.text
            else:
                print(f"API Call to {url} | Method: {method} | Failed. No response received.")
        except requests.exceptions.HTTPError as errh:
            print("HTTP Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Oops: Something Else", err)
