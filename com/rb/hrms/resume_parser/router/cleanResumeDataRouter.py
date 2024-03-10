from com.rb.hrms.resume_parser.exceptions.api_response import HRMSApiException
from com.rb.hrms.resume_parser.constants.FastApiResponseConstants import *
from com.rb.hrms.resume_parser.controllers.CandidateRawDataProcessor import CandidateRawDataProcessor
from fastapi import APIRouter

router = APIRouter()


@router.post("/hrms/cleanResumesData")
def Clean_Resume_Data():
    response = CandidateRawDataProcessor(Authorization=None,
                                         X_TenantID='redberyltech').process_candidate_raw_details()
    if response:
        api_response = HRMSApiException().valid_clean_resume_data_response(valid_json_response_clean_resume_data)
    else:
        api_response = HRMSApiException().invalid_clean_resume_data_response(invalid_json_response_clean_resume_data)
    return api_response
