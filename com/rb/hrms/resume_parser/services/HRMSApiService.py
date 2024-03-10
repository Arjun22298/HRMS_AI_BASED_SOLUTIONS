import json
import requests
from com.rb.hrms.resume_parser.logging.Logging_file import custom_logger
logger = custom_logger


class HRMSApiService:
    def __init__(self, base_url, username, password, jwt_token_id=None, X_TenantID=None):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.jwt_token = jwt_token_id
        self.X_TenantID = X_TenantID
        self.headers = None

    @custom_logger.log_around
    def form_headers(self):
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': "*/*",
            'X-TenantID': self.X_TenantID
        }
        if self.jwt_token:
            self.jwt_token = self.jwt_token.split('Bearer ')[-1]
            self.headers['Authorization'] = f'Bearer {self.jwt_token}'
        # self.hrms_headers = self.headers
        return self.headers

    @custom_logger.log_around
    def get_headers(self):
        return self.headers

    @custom_logger.log_around
    def login(self):
        if not self.jwt_token:
            clean_flag = False
            login_url = f'{self.base_url}/api/user/signin'
            credentials = {
                "username": self.username,
                "password": self.password
            }
            response = requests.post(login_url, json=credentials, headers=self.form_headers())
            if response.status_code == 201:
                jwt_token = response.json().get('accessToken')
                # self.form_headers()
                self.headers['Authorization'] = f'Bearer {jwt_token}'

                print("Login Successful. JWT Token obtained.")
            else:
                print(f"Login Failed. Status Code: {response.status_code}, Message: {response.text}")
        else:
            print('Skipping login. JWT Token already available.')
            clean_flag = True
            self.form_headers()
        return clean_flag

    @custom_logger.log_around
    def logout(self):
        if self.jwt_token is not None:
            print("Skipping logout. JWT Token already available.")
        else:

            logout_url = f'{self.base_url}/api/user/logout'
            response = requests.post(logout_url, headers=self.get_headers())

            if response.status_code == 200:
                print("Logout Successful.")
            else:
                print(f"Logout Failed. Status Code: {response.status_code}, Message: {response.text}")

    @custom_logger.log_around
    def hrms_api_call(self, headers, method, url, data=None):
        try:
            print(type(data))
            json_data = json.dumps(data)
            response = requests.request(headers=headers, method=method, data=json_data, url=url)
            response.raise_for_status()
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



"""x = HRMSApiService('http://192.168.1.102:8082', 'redberyltech1234', 'redberyltech@1234', None,
                   X_TenantID='redberyltech')
x.login()


x.logout()
"""