import os
from com.rb.hrms.resume_parser.models.RequestData import RequestData
from com.rb.hrms.resume_parser.services.ResumeParserWithAIService import ResumeParserWithAIService
from com.rb.hrms.resume_parser.exceptions.api_response import HRMSApiException
from com.rb.hrms.resume_parser.constants.FastApiResponseConstants import *

from fastapi import APIRouter

router = APIRouter()


@router.post("/hrms/ResumeParsingProcessor")
def resume_processing(request: RequestData):
    # print(request)
    if not os.path.exists(request.download_resume_folder):
        api_response = HRMSApiException().invalid_resume_data_parsing_response(invalid_json_response_resume_parsing)
    resume_success, resume_failed = ResumeParserWithAIService(Authorization=None, X_TenantID=None).process_resumes(
        request.download_resume_folder)
    if resume_success or resume_failed:
        resume_json_response = {"status": resume_success, "failed": resume_failed}
        api_response = HRMSApiException().valid_resume_data_parsing_response(resume_json_response)

    return api_response
