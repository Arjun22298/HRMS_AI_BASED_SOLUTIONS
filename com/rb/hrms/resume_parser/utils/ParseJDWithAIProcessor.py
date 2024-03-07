import glob
import os
import logging
from com.rb.hrms.resume_parser.utils.FileProcessor import FileProcessor
from com.rb.hrms.resume_parser.utils.JDResponseHandler import JDResponseHandler
from com.rb.hrms.resume_parser.services.HRMSAIService import AIService
from com.rb.hrms.resume_parser.constants.JDParsingWithAiConstants import JOB_DESCRIPTION_DETAILS
from com.rb.hrms.resume_parser.logging.Logging_file import custom_logger

logger = custom_logger


class ParseJDWithAIProcessor:
    @custom_logger.log_around
    def parsed_JD(self, folder_path):
        try:
            list_of_files = glob.glob(f'{folder_path}\\*.*')
            for file in list_of_files:
                file_extension = os.path.splitext(file)[-1].lower()
                if file_extension == '.pdf':
                    data = FileProcessor().pdf(file)
                elif file_extension == '.docx' or file_extension == '.doc':
                    data = FileProcessor().word(file)
                else:
                    logging.warning(f"Unsupported file format: {file_extension}")
                    continue
                # TODO - -- > AI WILL PARSED THE JD AND GIVEN ME ACCURATE FORMAT ..
                try:
                    self.ai_service = AIService('gemini')
                    self.ai_service.login()
                    response = self.ai_service.ai_api_call(f"{data},{JOB_DESCRIPTION_DETAILS}")
                    handling_response_of_jd_parser = JDResponseHandler()
                    response = handling_response_of_jd_parser._handling_jd_ai_response(response, file)
                    # TODO ---> RETURN THE  OF DATA
                    if response:
                        return response
                except Exception as e:
                    logging.warning(f'Exception comes from Parsed based on JD {str(e)}')
                finally:
                    self.ai_service.logout()
        except Exception as e:
            print("Exception error comes", str(e))


x = ParseJDWithAIProcessor().parsed_JD('D:\JobDescriptionFile')
print(x)
