from fastapi import HTTPException
from com.rb.hrms.resume_parser.controllers.CleanCandidateRawDetailsController import APIProcessor
from com.rb.hrms.resume_parser.models.RequestData import RequestData
from com.rb.hrms.resume_parser.exceptions.api_response import HRMSApiException
from com.rb.hrms.resume_parser.constants.FastApiResponseConstants import *

from fastapi import APIRouter

router = APIRouter()


@router.post("/resume_parser_callable")
def process_request(data: RequestData):
    try:
        # x_api_key: str = Header(..., convert_underscores=False)
        processor = APIProcessor(None)
        print("This is the data ", data)
        processor.process_request(data)
        api_response = HRMSApiException().valid_resume_data_parsing_response(valid_json_response_of_email_resume)
        return api_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))








