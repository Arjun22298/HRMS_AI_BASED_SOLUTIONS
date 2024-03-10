import os
from fastapi import Header
from com.rb.hrms.resume_parser.services.ResumeParserWithAIService import ResumeParserWithAIService
from com.rb.hrms.resume_parser.exceptions.api_response import HRMSApiException
from com.rb.hrms.resume_parser.constants.FastApiResponseConstants import *

from fastapi import APIRouter

router = APIRouter()


@router.post("/hrms/ParsedSingleResume")
async def parse_single_resume(Authorization: str = Header(None), X_TenantID: str = Header(None)):
    resume_file_path = 'D:\Single_Resume_Folder'
    if not os.path.exists(resume_file_path):
        api_response = HRMSApiException().generate_resume_parsing_invalid_exception(invalid_resume_file_path)
        return api_response
    data = ResumeParserWithAIService(Authorization=None, X_TenantID='redberyltech').process_single_resume(
        resume_file_path)
    if data is not None and (data[0]['CVs processed'] > 0 or data[1]['CVs processed'] > 0):
        api_response = HRMSApiException().valid_parse_jd_response(json_response_single_parse_resume_success)
    else:
        api_response = HRMSApiException().generate_resume_parsing_invalid_exception(
            json_response_single_parse_resume_failed)

    return api_response
