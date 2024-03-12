from com.rb.hrms.resume_parser.services.HRMSAIService import AIService
from com.rb.hrms.resume_parser.constants.AiApiConstant import *
from com.rb.hrms.resume_parser.constants.HRMSApiConstants import *
import json
import logging
import ast
from com.rb.hrms.resume_parser.logging.Logging_file import custom_logger

logger = custom_logger


class QualificationService:
    @custom_logger.log_around
    def _ai_cleaning_qualification_name(self, hrms_api_service, qualification_name):
        try:
            self.ai_service = AIService('gemini')
            self.ai_service.login()
            print("Gemiai is working fine ", self.ai_service.login())
            qualification_response = self.ai_service.ai_api_call(
                f"{SEARCH_QUALIFICATION_PROMPT_PART1} {qualification_name} {SEARCH_QUALIFICATION_PROMPT_PART2} {SEARCH_QUALIFICATION_RESPONSE_JSON} {SEARCH_QUALIFICATION_PROMPT_PART3}")
            clean_qualification_response = self.clean_qualification_response(qualification_response)
            if clean_qualification_response:
                qualification_name = clean_qualification_response.get('qualification_description')
                clean_qualification_response = self.search_qualification_in_master(hrms_api_service=hrms_api_service,
                                                                                   qualification_name=qualification_name)

            # TODO --> AFTER THAT GET THE NAME OF QUALIFICATION NAME AND QUALIFICATION DESCRIPTION
            # TODO --> SEARCH BASED ON QUALIFICATION DESCRIPTION
            #  CALLING API TO SEARCH QUALIFICATION IN MASTER TABLE
            #  IF RESPONSE IS NONE  CALL THE API TO INSERT THE DATA INTO MASTER OF QUALIFICATION TABLE AND RETURN JSON
            return clean_qualification_response
        except Exception as e:
            logging.error(str(e), exc_info=True)

    @custom_logger.log_around
    def clean_qualification_response(self, qualification_response):
        try:
            self.response = qualification_response
            # TODO --> CALLING THE HANDLING THE RESPONSE OF AI
            clean_qualification_response = self.response.replace('```', "").replace('json', "").replace('JSON',
                                                                                                        "").replace(
                '\n', '')
            # TODO -- CHECK IF CLEAN QUALIFICATION RESPONSE IS ALREADY DICT FORMAT
            if isinstance(clean_qualification_response, dict):
                json_response_for_qualification = clean_qualification_response
            else:
                try:
                    # TODO Safely evaluate the string representation into a dictionary
                    json_response_for_qualification = ast.literal_eval(clean_qualification_response)
                except ValueError:
                    # TODO If ast.literal_eval() fails, the string might not be valid Python syntax, so treat it as JSON
                    try:
                        json_response_for_qualification = json.loads(clean_qualification_response)
                    except json.JSONDecodeError:
                        # TODO If both ast.literal_eval() and json.loads() fail, the string is not a valid JSON,
                        #  handle as needed
                        print("Invalid data format")

            qualification_name = json_response_for_qualification.get('name', '').upper()
            self.qualification_description = json_response_for_qualification.get('description', '').upper()
            if qualification_name and self.qualification_description is not None:
                response = {"qualification_name": qualification_name,
                            "qualification_description": self.qualification_description}
            else:
                return None
            return response

        except Exception as e:
            logging.error('Exception error found JSON NOT RESPONSE ON FILTER AI RESPONSE: %s', str(e))
            """clean_qualification_json_response = json.loads(self.clean_qualification_response)
            json_response_for_qualification = clean_qualification_json_response"""

    @custom_logger.log_around
    def search_qualification_in_master(self, hrms_api_service, qualification_name):
        try:
            url = f"{hrms_api_service.base_url}/{SEARCH_QUALIFICATION_BY_NAME_API_END_POINT}"
            payload = {
                "nameOrDescription": qualification_name
            }
            response = hrms_api_service.hrms_api_call(headers=hrms_api_service.headers, method='GET',
                                                      url=url, data=payload)
            if response is None:
                response = self.insert_qualification_name_in_master(hrms_api_service, qualification_name,
                                                                    self.qualification_description)
            return response

        except Exception as e:
            logging.error(str(e), exc_info=True)
            return None

    @custom_logger.log_around
    def insert_qualification_name_in_master(self, hrms_api_service, qualification_name, qualification_description):
        try:

            url = f"{hrms_api_service.base_url}/{INSERT_QUALIFICATION_API_END_POINT.format(name=qualification_name, qualification_description=qualification_description)}"
            payload = {"name": qualification_name,
                       "description": qualification_description,
                       "isActive": True}
            response = hrms_api_service.hrms_api_call(headers=hrms_api_service.headers, method='POST',
                                                      url=url, data=payload)
            if response:
                return response
            else:
                return None
        except Exception as e:
            logging.error(str(e), exc_info=True)
            return None


"""x = QualificationService().clean_qualification_response(
    "{'name': 'B.E.', 'description': 'Bachelor of Engineering in Computer Science'}")
print("Response", x)"""
