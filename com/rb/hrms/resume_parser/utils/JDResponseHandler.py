import json
import os
from datetime import datetime
import shutil
import logging
from com.rb.hrms.resume_parser.constants.JDParsingWithAiConstants import *
from com.rb.hrms.resume_parser.services.ParsedJDAIService import ParsedJDAIService
from com.rb.hrms.resume_parser.logging.Logging_file import custom_logger

logger = custom_logger


class JDResponseHandler:
    @custom_logger.log_around
    def _handling_jd_ai_response(self, response, file):
        try:
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
                                    'skills': JD_skills,
                                    'filePath': file_directory_name, 'isActive': True}
                # TODO HERE WE CALL THE REMAINING SERVICE TO CALL THAT AND EXTRACT THE INFORMATION FOR THE DESCRIPTION
                if parse_jd_details:
                    self.insert_jd_data_into_database.generate_JD_response_based_on_HRMS_API(parse_jd_details)
                    return parse_jd_details
                return None

        except Exception as e:
            logging.error(f"Exception occurred handling AI response for job description: {str(e)}")
