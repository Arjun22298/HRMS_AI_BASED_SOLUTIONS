import requests
import json
from com.rb.hrms.resume_parser.constants.AiApiConstant import *
from com.rb.hrms.resume_parser.constants.HRMSApiConstants import *
import logging
from com.rb.hrms.resume_parser.services.HRMSAIService import AIService


class CityService:
    def cleanData(self, hrms_api_service, city_name):
        try:
            self.ai_service = AIService('gemini')
            response = self.seach_city_in_master(hrms_api_service, city_name)
            if response is None:
                self.ai_service.login()
                # TODO - Call AI Service
                response = self.ai_service.ai_api_call(
                    f"{CITY_DETAILS_PROMPT_PART1} {city_name} {CITY_DETAILS_PROMPT_PART2} {CITY_DETAILS_RESPONSE_FORMAT}")
                print(f"AI RESPONSE :: {response}")
                if response is None:
                    pass
                    # TODO - Insert data into city Master
                else:
                    city_name = self.get_clean_city_name(response)
                    response = self.seach_city_in_master(hrms_api_service, city_name)  # search
                    print(f"Response :: {response}")
                    if response is None:
                        response = self.insert_city_in_master(hrms_api_service, city_name)
            return response
        except Exception as e:
            logging.error(str(e))

    def seach_city_in_master(self, hrms_api_service, city_name):
        try:
            url = f"{hrms_api_service.base_url}/{SEARCH_CITY_BY_NAME_API_END_POINT}"
            print(f"URL :: {url}")

            json_body_of_city = {"cityName": city_name}

            response = hrms_api_service.hrms_api_call(headers=hrms_api_service.headers, method='GET',
                                                      url=url, data=json_body_of_city)
            if response:
                return response
        except Exception as e:
            logging.error(str(e), exc_info=True)
            return None

    def insert_city_in_master(self, hrms_api_service, city_name):
        try:

            url = f"{hrms_api_service.base_url}/{INSERT_CITY_API_END_POINT.format(city_name=city_name)}"
            print(f"URL :: {url}")
            payload = {"cityName": city_name,
                       "isActive": True}
            print(type(payload))
            response = hrms_api_service.hrms_api_call(headers=hrms_api_service.headers, method='POST',
                                                      url=url, data=json.dumps(payload))
            if response:
                return response
        except Exception as e:
            logging.error(str(e), exc_info=True)
            return None

    def get_clean_city_name(self, response):
        try:
            self.city_response = response
            print(self.city_response)
            logging.info(self.city_response)
            clean_city_response = self.city_response.replace('```', "").replace('json', "").replace('JSON',
                                                                                                    "").replace(
                '\n', '')
            city_data = json.loads(clean_city_response)
            if 'city_name' in city_data and city_data['city_name'] is not None:
                city_data['city_name'] = city_data['city_name'].upper()

            logging.info(f"city information {city_data}")
            city_name = city_data.get('city_name')

            return city_name

        except Exception as e:
            print("Exception occurect while processing ai response...")
            print(e)
            return None
