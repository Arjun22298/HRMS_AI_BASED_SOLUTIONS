from uvicorn import run
from com.rb.hrms.resume_parser.controllers.CandidateRawDataProcessor import CandidateRawDataProcessor
import os
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status, HTTPException, Header
from com.rb.hrms.resume_parser.services.GmailService import GmailService
from fastapi.middleware.cors import CORSMiddleware
from com.rb.hrms.resume_parser.models.RequestData import RequestData, SingleResumeParsing
from com.rb.hrms.resume_parser.services.ResumeParserWithAIService import ResumeParserWithAIService
from com.rb.hrms.resume_parser.exceptions.api_response import HRMSApiException


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

origins = [
    "http://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/resume_parser_callable")
def process_request(data: RequestData):
    try:
        # x_api_key: str = Header(..., convert_underscores=False)
        processor = APIProcessor(None)
        print("This is the data ", data)
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
    resume_success, resume_failed = ResumeParserWithAIService(Authorization=None, X_TenantID=None).process_resumes(
        request.download_resume_folder)
    json_response = HRMSApiException().insert_data_in_database("Job Completed")
    if resume_success or resume_failed:
        json_response = {"status": resume_success, "failed": resume_failed}
        return JSONResponse(content=json_response, media_type='application/json')
    return json_response


@app.post("/hrms/cleanResumesData")
def Clean_Resume_Data():
    try:
        Authorization = 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJzYXVteWFAZHJkby5jb20iLCJpYXQiOjE3MDk3MTk2NTQsImV4cCI6MTcwOTc2Mjg1NH0.DCDBdrWUKEL0y5a_bN-sXaRbyZKT1bWesJo8M-rHf1xgApAeoFXnQJg1UN1rfjrOUTXJlmQyMn_vsYVMs05OKA'
        X_TenantID = 'drdo'
        response = CandidateRawDataProcessor(Authorization, X_TenantID).process_candidate_raw_details()
        print(response)
        json_response = {"status_code": status.HTTP_201_CREATED, "processing_status": "Request processed successfully"}
        return JSONResponse(content=json_response, status_code=status.HTTP_201_CREATED, media_type='application/json')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/hrms/ParsedSingleResume")
async def parse_resume(Authorization: str = Header(None), X_TenantID: str = Header(None)):
    resume_file_path = 'D:\Single_Resume_Folder'
    if not os.path.exists(resume_file_path):
        json_response = {'status_code': status.HTTP_404_NOT_FOUND, "processing_status": "File path does not exist"}
        return JSONResponse(content=json_response, status_code=status.HTTP_404_NOT_FOUND, media_type='application/json')
    data = ResumeParserWithAIService(Authorization, X_TenantID).process_single_resume(resume_file_path)
    if data is not None and (data[0]['CVs processed'] > 0 or data[1]['CVs processed'] > 0):
        json_response = {"status_code": status.HTTP_201_CREATED, "processing_status": "Success"}
        return JSONResponse(content=json_response, status_code=status.HTTP_201_CREATED, media_type='application/json')
    else:
        json_response = {'status_code': status.HTTP_404_NOT_FOUND, "processing_status": "No data available"}
        return JSONResponse(content=json_response, status_code=status.HTTP_404_NOT_FOUND, media_type='application/json')


"""@app.post('/hrms/parseJobDescription')
def parse_JD(request:JD_folder_path):
    # TODO -> HERE COMES FOLDER PATH IN THE REQUEST BODY
    if not os.path.exists(JD_folder_path):
        json_response = {'status_code':status.HTTP_404_NOT_FOUND,'processing_status':"JD_Folder path does not exist"}
        return JSONResponse(content=json_response,status_code=status.HTTP_404_NOT_FOUND,media_type='application/json')
    jd_parse_daata = ParseJDWithAIProcessor().parsed_JD(folder_path=JD_folder_path)
    if jd_parse_daata:
        json_response = {"status_code": status.HTTP_201_CREATED, "processing_status": "Success"}
        return JSONResponse(content=json_response, status_code=status.HTTP_201_CREATED, media_type='application/json')
    else:
        json_response = {'status_code': status.HTTP_404_NOT_FOUND, "processing_status": "No data available"}
        return JSONResponse(content=json_response, status_code=status.HTTP_404_NOT_FOUND, media_type='application/json')"""

if __name__ == "__main__":
    run(app, host=str("192.168.1.106"), port=int(7000))
