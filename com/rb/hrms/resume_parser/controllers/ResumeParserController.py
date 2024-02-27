"""import os
import logging
import uvicorn
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, status, Request, HTTPException
from com.rb.hrms.resume_parser.models.RequestData import RequestData
from com.rb.hrms.resume_parser.services.ResumeParserWithAIService import ResumeParserWithAIService
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
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


@app.get("/hrms/parse_resume", status_code=status.HTTP_200_OK)
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


@app.post("/hrms/ResumeParsingProcessor")
def resume_processing(request: RequestData):
    #print(request)
    if not os.path.exists(request.download_resume_folder):
        json_response = {'status_code': status.HTTP_404_NOT_FOUND, "processing_status": "File path does not exist"}
        return JSONResponse(content=json_response, status_code=status.HTTP_404_NOT_FOUND, media_type='application/json')
    resume_success, resume_failed = ResumeParserWithAIService().process_resumes(request.download_resume_folder)
    json_response = {'status_code': status.HTTP_201_CREATED, 'processing_status': "Job Completed"}
    if resume_success or resume_failed:
        json_response = {"status": resume_success, "failed": resume_failed}
        return JSONResponse(content=json_response, media_type='application/json')


if __name__ == "__main__":
    uvicorn.run(app, host="192.168.1.106", port=int(2000))"""
