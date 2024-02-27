import json
import requests
import google.generativeai as genai
from com.rb.hrms.resume_parser.constants.AiApiConstant import GOOGLE_API_KEY


class AIService:
    def __init__(self, service_type):
        self.service_type = service_type
        self.logged_in = False
        self.model = None

    def login(self):
        if self.service_type == 'gemini':
            genai.configure(api_key=GOOGLE_API_KEY)
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    pass
            self.model = genai.GenerativeModel('gemini-pro')
            self.logged_in = True

        elif self.service_type == 'chatGPT':
            # ChatGPT login logic
            # ...
            self.logged_in = True
        else:
            raise ValueError("Unsupported service type")

    def logout(self):
        # Implement logout logic based on the service_type
        if self.logged_in:
            if self.service_type == 'gemini':
                # Gemini logout logic
                # ...
                pass
            elif self.service_type == 'chatGPT':
                # ChatGPT logout logic
                # ...
                pass
            else:
                raise ValueError("Unsupported service type")
            self.logged_in = False

    def ai_api_call(self, input_string):
        try:
            split_array = input_string.split('##@##')

            # Iterate over the array using a for loop
            response1 = ''
            for value in split_array:
                value = f"{value} {response1}"

                response = self.model.generate_content(value)
                response1 = response
                response_json = response1.text
            return response_json

        except Exception as e:
            print("Exception Occured:", e)


