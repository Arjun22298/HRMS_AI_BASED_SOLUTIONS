import logging
import glob
import os
import google.generativeai as genai
from com.rb.hrms.resume_parser.utils.ResumeParsingStatus import ResumeParsingStatus
from tenacity import retry, stop_after_attempt, wait_fixed
from com.rb.hrms.resume_parser.utils.FileProcessor import FileProcessor
from com.rb.hrms.resume_parser.constants.ResumeParsingWithAIConstants import PROMPT_TO_GET_INITIAL_DATA, \
    PROMPT_TO_GET_DATA_IN_JSON_FORMAT, API_KEY
from com.rb.hrms.resume_parser.constants.HRMSApiConstants import *
from com.rb.hrms.resume_parser.services.HRMSApiService import HRMSApiService


class ResumeProcessor:
    def __init__(self, JWT_TOKEN_ID, X_TenantID):
        self.GOOGLE_API_KEY = API_KEY
        genai.configure(api_key=self.GOOGLE_API_KEY)

        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                pass
        self.model = genai.GenerativeModel('gemini-pro')
        self.setup_logger()

        self.api_caller = HRMSApiService(base_url=API_BASE_URL, username=HRMS_API_USERNAME,
                                         password=HRMS_API_PASSWORD, jwt_token_id=JWT_TOKEN_ID, X_TenantID=X_TenantID)

    def setup_logger(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1), reraise=True)
    def generate_content_with_retry(self, data):
        return self.model.generate_content(data)

    # TODO --INSERT RAW DATA INTO DATABASE ... AND AFTER INSERT THE DATA INTO TABLE API WILL LOG OUT ..

    # TODO ---> PROCESSING THE FILE AND AFTER PARSING THE RESUME INSERT INTO RAW CANDIDATE DATA.
    def process(self, folder_path):
        try:
            self.api_caller.login()
            self.response_json = ResumeParsingStatus()
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
                self.handle_single_resume(data, file)
            self.list_of_data = self.response_json.list_of_json_data
            success_count, failed_count = self.response_json.process_cv()
            return success_count, failed_count

        except Exception as e:
            logging.warning(f"exception comes from processed_resumes{str(e)}")

        finally:
            self.api_caller.logout()

    def handle_single_resume(self, resume_parsed_text, file):
        try:
            response = self.generate_content_with_retry(
                f"{resume_parsed_text},{PROMPT_TO_GET_INITIAL_DATA} i given you Structure should we "
                f"followed This Structure{PROMPT_TO_GET_DATA_IN_JSON_FORMAT} Json Structure")
            self.resume_data = response.text
            self.response_json.handle_response(self.resume_data, file, hrms_api_service=self.api_caller)

        except Exception as e:
            logging.warning("Exception comes on _handling_Response Data", str(e))
            response_file = self.generate_content_with_retry(
                f"{self.resume_data} Please Give me in Proper Json Format")
            candidate_response_data_2 = response_file.text
            logging.info("Exception candidate_Response_data", candidate_response_data_2)
            self.response_json.handle_response(candidate_response_data_2, file, hrms_api_service=self.api_caller)
            return candidate_response_data_2


"""x = ResumeProcessor().process('D:\RESUME_DOWNLOAD_PATH')"""
