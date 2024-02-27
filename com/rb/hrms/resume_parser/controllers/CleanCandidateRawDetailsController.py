from fastapi import FastAPI, HTTPException
from uvicorn import run
from fastapi.responses import JSONResponse
from com.rb.hrms.resume_parser.services.HRMSApiService import HRMSApiService
from fastapi import FastAPI, HTTPException, Header
from com.rb.hrms.resume_parser.models.RequestData import RequestData
from fastapi import status
from com.rb.hrms.resume_parser.controllers.CandidateRawDataProcessor import CandidateRawDataProcessor
import os
import logging
import uvicorn
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, status, Request, HTTPException

from com.rb.hrms.resume_parser.services.GmailService import GmailService
from com.rb.hrms.resume_parser.models.RequestData import RequestData
from com.rb.hrms.resume_parser.services.ResumeParserWithAIService import ResumeParserWithAIService


class APIProcessor:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id

    def process_request(self, request_data: RequestData):
        # Your processing logic here
        # For demonstration purposes, we will print the data and API key
        print(f"Processing request with data: {request_data.dict()}")
        print(f"API Key: {self.tenant_id}")
        if request_data.email_account_name.lower() == "gmail":
            print("I am in GMAIL Call...")
            emailService = GmailService()
        else:
            pass
            # emailService = OutlookService()
        try:
            emailService.process(request_data)
        except Exception as e:
            print(e)


app = FastAPI()


@app.post("/resume_parser_callable")
def process_request(data: RequestData):
    try:
        # x_api_key: str = Header(..., convert_underscores=False)
        processor = APIProcessor(None)
        print("This is the data ",data)
        processor.process_request(data)
        json_response = {"status_code": status.HTTP_201_CREATED, "processing_status": "Request processed successfully"}
        return JSONResponse(content=json_response, status_code=status.HTTP_202_ACCEPTED, media_type='application/json')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/hrms/ResumeParsingProcessor")
def resume_processing(request: RequestData):
    # print(request)
    if not os.path.exists(request.download_resume_folder):
        json_response = {'status_code': status.HTTP_404_NOT_FOUND, "processing_status": "File path does not exist"}
        return JSONResponse(content=json_response, status_code=status.HTTP_404_NOT_FOUND, media_type='application/json')
    resume_success, resume_failed = ResumeParserWithAIService().process_resumes(request.download_resume_folder)
    json_response = {'status_code': status.HTTP_201_CREATED, 'processing_status': "Job Completed"}
    if resume_success or resume_failed:
        json_response = {"status": resume_success, "failed": resume_failed}
        return JSONResponse(content=json_response, media_type='application/json')


@app.post("/hrms/cleanResumesData")
def Clean_Resume_Data(request: str = None):
    try:
        response = CandidateRawDataProcessor().process_candidate_raw_details()
        print(response)
        json_response = {"status_code": status.HTTP_201_CREATED, "processing_status": "Request processed successfully"}
        return JSONResponse(content=json_response, status_code=status.HTTP_201_CREATED, media_type='application/json')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/hrms/parse_resume", status_code=status.HTTP_200_OK)
def parse_resume():
    resume_file_path = 'D:\RESUME_DOWNLOAD_PATH'
    if not os.path.exists(resume_file_path):
        json_response = {'status_code': status.HTTP_404_NOT_FOUND, "processing_status": "File path does not exist"}
        return JSONResponse(content=json_response, status_code=status.HTTP_404_NOT_FOUND, media_type='application/json')
    data = ResumeParserWithAIService().process_resumes(resume_file_path)
    if data is not None and (data[0]['CVs processed'] > 0 or data[1]['CVs processed'] > 0):
        json_response = {"status_code": status.HTTP_201_CREATED, "processing_status": "Success"}
        return JSONResponse(content=json_response, status_code=status.HTTP_201_CREATED, media_type='application/json')
    else:
        json_response = {'status_code': status.HTTP_404_NOT_FOUND, "processing_status": "No data available"}
        return JSONResponse(content=json_response, status_code=status.HTTP_404_NOT_FOUND, media_type='application/json')



if __name__ == "__main__":
    run(app, host=str("192.168.1.106"), port=int(7000))
