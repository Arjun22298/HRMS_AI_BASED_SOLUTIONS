import requests
import json
from com.rb.hrms.resume_parser.constants.AiApiConstant import *
from com.rb.hrms.resume_parser.constants.HRMSApiConstants import *
import logging
from com.rb.hrms.resume_parser.services.HRMSAIService import AIService
from com.rb.hrms.resume_parser.logging.Logging_file import custom_logger

logger = custom_logger


class SkillService:
    @custom_logger.log_around
    def cleanData(self, hrms_api_service, skill_name):
        try:
            self.ai_service = AIService('gemini')
            self.ai_service.login()
            # TODO - Call AI Service
            response = self.ai_service.ai_api_call(
                f"{SKILL_DETAILS_PROMPT_PART1} {skill_name} {SKILL_DETAILS_PROMPT_PART2} {SKILL_DETAILS_RESPONSE_FORMAT}")
            print(f"AI RESPONSE :: {response}")
            if response is None:
                pass
                    # TODO - Insert data into SKILLS Master
            else:
                skill_name = self.get_clean_skill_name(response)
                response = self.search_skill_in_master(hrms_api_service, skill_name)  # search
                print(f"Response :: {response}")
                if response is None:
                    response = self.insert_skills_in_master(hrms_api_service, skill_name)
            return response
        except Exception as e:
            logging.error(str(e))

    @custom_logger.log_around
    def search_skill_in_master(self, hrms_api_service, skill_name):
        try:
            url = f"{hrms_api_service.base_url}/{SEARCH_SKILLS_BY_NAME_API_END_POINT}"

            json_body_for_skill = {"skillName": skill_name}

            response = hrms_api_service.hrms_api_call(headers=hrms_api_service.headers, method='GET',
                                                      url=url, data=json_body_for_skill)
            if response:
                return response
        except Exception as e:
            logging.error(str(e), exc_info=True)
            return None

    @custom_logger.log_around
    def insert_skills_in_master(self, hrms_api_service, skill_name):
        try:

            url = f"{hrms_api_service.base_url}/{INSERT_SKILLS_API_END_POINT.format(skill_name=skill_name)}"
            payload = {"skillName": skill_name,
                       "isActive": True}
            response = hrms_api_service.hrms_api_call(headers=hrms_api_service.headers, method='POST',
                                                      url=url, data=payload)
            if response:
                return response
        except Exception as e:
            logging.error(str(e), exc_info=True)
            return None

    @custom_logger.log_around
    def get_clean_skill_name(self, response):
        try:
            self.skill_response = response
            logging.info(self.skill_response)
            clean_skills_response = self.skill_response.replace('```', "").replace('json', "").replace('JSON',
                                                                                                       "").replace(
                '\n', '')
            skill_data = json.loads(clean_skills_response)
            if 'skill_name' in skill_data and skill_data['skill_name'] is not None:
                skill_data['skill_name'] = skill_data['skill_name'].upper()
            logging.info(f"skills information {skill_data}")
            skill_name = skill_data.get('skill_name')

            return skill_name

        except Exception as e:
            print("Exception occurrence while processing ai response...")
            print(e)
            return None
