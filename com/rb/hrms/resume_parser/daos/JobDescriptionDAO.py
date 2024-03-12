from com.rb.hrms.resume_parser.services.HRMSApiService import HRMSApiService
from com.rb.hrms.resume_parser.constants.HRMSApiConstants import API_BASE_URL, HRMS_API_PASSWORD, HRMS_API_USERNAME


class jobDescriptionDao:
    def __init__(self, authorization, X_TenantID):
        self.authorization = authorization
        self.x_tenantid = X_TenantID
        self.hrms_api_service = HRMSApiService(base_url=API_BASE_URL, username=HRMS_API_USERNAME,
                                               password=HRMS_API_PASSWORD, jwt_token_id=self.authorization,
                                               X_TenantID=self.x_tenantid)
