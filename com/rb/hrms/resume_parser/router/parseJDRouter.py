import os
from com.rb.hrms.resume_parser.exceptions.api_response import HRMSApiException
from com.rb.hrms.resume_parser.utils.ParseJDWithAIProcessor import ParseJDWithAIProcessor
from com.rb.hrms.resume_parser.constants.FastApiResponseConstants import *

from fastapi import APIRouter

router = APIRouter()


@router.post('/hrms/parseJobDescription')
def parse_JD():
    # TODO -> HERE COMES FOLDER PATH IN THE REQUEST BODY
    JD_folder_path = 'D:\JobDescriptionFile'
    if not os.path.exists(JD_folder_path):
        api_response = HRMSApiException().invalid_jd_response(invalid_file_json_response_jd)
        return api_response
    parsed_data = ParseJDWithAIProcessor(Authorization=None, X_TenantID='redberyltech').parsed_JD(
        folder_path=JD_folder_path)
    if parsed_data is None:
        api_response = HRMSApiException().invalid_jd_response(invalid_json_response_jd)
    else:
        jd_parse_data, clean_flag = parsed_data
        valid_json_response_jd = {"processing_status": "Success", 'jd_response_data': jd_parse_data,
                                  'clean_flag': clean_flag}
        api_response = HRMSApiException().valid_parse_jd_response(valid_json_response_jd)
    return api_response
