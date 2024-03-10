from com.rb.hrms.resume_parser.services.GmailService import GmailService
from com.rb.hrms.resume_parser.models.RequestData import RequestData


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


"""app = FastAPI()

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
        api_response = HRMSApiException().valid_resume_data_parsing_response(valid_json_response_of_email_resume)
        return api_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/hrms/ResumeParsingProcessor")
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


@app.post("/hrms/cleanResumesData")
def Clean_Resume_Data():
    response = CandidateRawDataProcessor(Authorization=None,
                                         X_TenantID='redberyltech').process_candidate_raw_details()
    if response:
        api_response = HRMSApiException().valid_clean_resume_data_response(valid_json_response_clean_resume_data)
    else:
        api_response = HRMSApiException().invalid_clean_resume_data_response(invalid_json_response_clean_resume_data)
    return api_response


@app.post("/hrms/ParsedSingleResume")
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


@app.post('/hrms/parseJobDescription')
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


if __name__ == "__main__":
    run(app, host=str("192.168.1.106"), port=int(7000))
"""
