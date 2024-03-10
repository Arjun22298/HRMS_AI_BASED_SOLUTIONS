import json
import os
from datetime import datetime
import shutil
import logging
from com.rb.hrms.resume_parser.services.HRMSApiService import HRMSApiService
from com.rb.hrms.resume_parser.constants.JDParsingWithAiConstants import *
from com.rb.hrms.resume_parser.services.ParsedJDAIService import ParsedJDAIService
from com.rb.hrms.resume_parser.logging.Logging_file import custom_logger
from com.rb.hrms.resume_parser.constants.HRMSApiConstants import API_BASE_URL, HRMS_API_PASSWORD, HRMS_API_USERNAME

logger = custom_logger


class JDResponseHandler:
    def __init__(self, Authorization, X_TenantID):
        self.authorization = Authorization
        self.x_tenantid = X_TenantID

    @custom_logger.log_around
    def _handling_jd_ai_response(self, response, file):
        try:
            hrms_api_service = HRMSApiService(base_url=API_BASE_URL, username=HRMS_API_USERNAME,
                                              password=HRMS_API_PASSWORD, jwt_token_id=self.authorization,
                                              X_TenantID=self.x_tenantid)
            hrms_api_service.login()
            self.insert_jd_data_into_database = ParsedJDAIService()
            file_name = os.path.basename(file)
            self.response = response
            self.clean_data = self.response.replace('```', "").replace('json', "").replace('JSON', "").replace('\n', '')
            json_data = json.loads(self.clean_data)
            if json_data.get('job_title') is not None:
                job_title = json_data['job_title'].upper()
            if json_data.get('Skills') is not None:
                JD_skills = json_data['Skills'].upper()
                processed_date = datetime.now().date()
                parsed_date = processed_date.strftime("%Y-%m-%d")
                destination_folder_path = os.path.abspath(DESTINATION_JD_FOLDER_PATH)
                # TODO --> DESTINATION JD FOLDER PATH ...

                file_directory_name = os.path.join(destination_folder_path, file_name)
                if os.path.exists(file_directory_name):
                    os.remove(file_directory_name)
                shutil.move(file, DESTINATION_JD_FILE_PATH)
                parse_jd_details = {'jobDescription': job_title, 'jsonData': json_data, 'date': parsed_date,
                                    'filePath': file_directory_name, 'isActive': True}

                # TODO HERE WE CALL THE REMAINING SERVICE TO CALL THAT AND EXTRACT THE INFORMATION FOR THE DESCRIPTION
                if parse_jd_details:
                    response, clean_flag = self.insert_jd_data_into_database.generate_JD_response_based_on_HRMS_API(
                        hrms_api_service=hrms_api_service, JD_parse_data=parse_jd_details)

                    return response, clean_flag

        except Exception as e:
            logging.error(f"Exception occurred handling AI response for job description: {str(e)}")
        finally:
            hrms_api_service.logout()
