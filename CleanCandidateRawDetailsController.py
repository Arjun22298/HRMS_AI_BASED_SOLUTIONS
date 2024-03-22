from com.rb.hrms.resume_parser.services.GmailService import GmailService
from com.rb.hrms.resume_parser.models.RequestData import RequestData


class APIProcessor:

    def process_request(self, request_data: RequestData):
        # Your processing logic here
        # For demonstration purposes, we will print the data and API key
        print(f"Processing request with data: {request_data.dict()}")
        if request_data.email_account_name.lower() == "gmail":
            print("I am in GMAIL Call...")
            self.emailService = GmailService()
        else:
            pass
            # emailService = OutlookService()
        try:
            response = self.emailService.process(request_data)
            return response
        except Exception as e:
            print(e)

