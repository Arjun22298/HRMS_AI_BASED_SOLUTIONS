from com.rb.hrms.resume_parser.services.HRMSAIService import AIService
from com.rb.hrms.resume_parser.constants.JDvsCVAIConstants import *
from datetime import datetime


class JDvsCVAIBasedCompare:
    def __init__(self):
        pass

    def parsed_ai_jd_vs_cv_data(self, jd_json_data, candidate_raw_json_data):
        try:
            self.ai_service = AIService('gemini')
            self.ai_service.login()
            response = self.ai_service.ai_api_call(f"{TITLE_JD} {jd_json_data}. Based on {jd_json_data}."
                                                   f" {COMPARE_JD} {candidate_raw_json_data} {RESULT_JD}"
                                                   f" {JOB_DESCRIPTION_DETAILS} and {EXPERIENECE_DATA} "
                                                   f"{JSON_FORMAT}")
            response = response.replace('\n', "")
            processed_date = datetime.now().date()
            print("This is the response of jd details", response, processed_date)

            return response, processed_date
            # response_of_jd, clean_flag = handling_response_of_jd_parser._handling_jd_ai_response(response, file)


        except Exception as e:
            print("Exceptions comes of JD_CV_AI_COMPRESSION", str(e))
