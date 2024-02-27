"""from fastapi import FastAPI, HTTPException
from uvicorn import run
from fastapi.responses import JSONResponse
from com.rb.hrms.resume_parser.services.GmailService import GmailService
from com.rb.hrms.resume_parser.services.OutlookService import OutlookService
from fastapi import FastAPI, HTTPException, Header
from com.rb.hrms.resume_parser.models.RequestData import RequestData
from fastapi import status


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
            #emailService = OutlookService()
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
        processor.process_request(data)
        json_response = {"status_code": status.HTTP_201_CREATED, "processing_status": "Request processed successfully"}
        return JSONResponse(content=json_response, status_code=status.HTTP_202_ACCEPTED, media_type='application/json')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    run(app, host=str("192.168.1.106"), port=int(7000))
"""

