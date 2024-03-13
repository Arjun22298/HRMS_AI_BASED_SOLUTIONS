from com.rb.hrms.resume_parser.constants.HRMSApiConstants import *
from com.rb.hrms.resume_parser.constants.HRMSApiConstants import API_BASE_URL, HRMS_API_PASSWORD, HRMS_API_USERNAME
from com.rb.hrms.resume_parser.services.HRMSApiService import HRMSApiService
from com.rb.hrms.resume_parser.logging.Logging_file import custom_logger

logger = custom_logger


class JDvsCVComparisonDAO:

    def __init__(self, X_TenantID):
        self.x_tenantid = X_TenantID
        self.hrms_api_service = HRMSApiService(base_url=API_BASE_URL, username=HRMS_API_USERNAME,
                                               password=HRMS_API_PASSWORD,
                                               X_TenantID=self.x_tenantid)

    @custom_logger.log_around
    def get_job_description_details(self, hrms_api_service):
        try:
            print("This is the value of hrms_api_service", hrms_api_service)
            url = f"{self.hrms_api_service.base_url}/{GET_JOB_DESCRIPTION_DETAILS_API_END_POINT}"
            response = self.hrms_api_service.hrms_api_call(headers=hrms_api_service, method='GET',
                                                           url=url)

            return response
        except Exception as e:
            print("An error occurred while getting job description details:", str(e))

    @custom_logger.log_around
    def get_candidate_raw_data_tables(self, hrms_api_service):
        try:
            url = f"{self.hrms_api_service.base_url}{GET_CANDIDATE_RAW_DETAILS_API_END_POINT}"
            response_candidate_raw_Table = self.hrms_api_service.hrms_api_call(headers=hrms_api_service,
                                                                               method='GET', url=url)
            return response_candidate_raw_Table
        except Exception as e:
            print("An error occurred while getting candidate raw data tables:", str(e))

    def insert_raw_data_of_JDvsCV_Comparison(self, hrms_api_service, payload):
        try:
            url = f"{hrms_api_service.base_url}/{INSERT_JD_VS_CV_COMPARSION_RAW_DATA_API_END_POINT}"
            response = hrms_api_service.hrms_api_call(headers=hrms_api_service.headers, method='POST',
                                                      url=url, data=payload)
            return response

        except Exception as e:
            print("Exception error comes in Insert raw data of jdvscv comparison", str(e))
