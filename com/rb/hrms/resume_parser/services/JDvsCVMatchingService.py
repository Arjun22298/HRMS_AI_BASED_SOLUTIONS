# TODO --- STEP 1. TO GET THE JD WHICH IS ACTIVE....
from com.rb.hrms.resume_parser.logging.Logging_file import custom_logger
from com.rb.hrms.resume_parser.constants.HRMSApiConstants import *
from com.rb.hrms.resume_parser.services.HRMSApiService import HRMSApiService
from com.rb.hrms.resume_parser.constants.HRMSApiConstants import API_BASE_URL, HRMS_API_PASSWORD, HRMS_API_USERNAME
from com.rb.hrms.resume_parser.utils.JD_vs_CV_AI_Based_Comparison import JDvsCVAIBasedCompare
from com.rb.hrms.resume_parser.daos.JDvsCVComparssionDAO import JDvsCVComparisonDAO

logger = custom_logger


class JDvsCVMatchingService:
    def __init__(self, X_TenantID):
        self.x_tenantid = X_TenantID
        self.hrms_api_service = JDvsCVComparisonDAO(self.x_tenantid)
    @custom_logger.log_around
    def get_job_description_details(self):
        try:
            self.hrms_api_service.hrms_api_service.login()
            self.headers = self.hrms_api_service.hrms_api_service.headers
            response = self.hrms_api_service.get_job_description_details(hrms_api_service=self.headers)
            if response:
                for jd_json in response:
                    if jd_json.get('isActive') == True:
                        job_description_json_data = jd_json['jsonData']
                        job_description_id = jd_json['id']
                        yield job_description_id,job_description_json_data
                    else:
                        None
                # return response
            else:
                return None
        except Exception as e:
            print("Exception comes on JDvsCVMatching service", str(e))
        finally:
            self.hrms_api_service.hrms_api_service.logout()
        # TODO ONLY GET  JOB DESCRIPTION DETAILS JSON IS ACTIVE WILL TRUE

    @custom_logger.log_around
    def _read_json_candidate_details(self):
        try:
            # TODO --- STEP 2. GET THE JD MATCHED WITH EACH OF CANDIDATE JSON DATA....
         for job_description_id,job_description_json_data in self.get_job_description_details():
             print(job_description_id,job_description_json_data)
             get_json_data_candidate_raw_table = self.hrms_api_service.get_candidate_raw_data_tables(hrms_api_service=self.headers)
             if get_json_data_candidate_raw_table:
                for json_data_candidate in get_json_data_candidate_raw_table:
                    print("This is the json data of candidate raw tables",json_data_candidate)
                    if json_data_candidate['candidateDetails_id']:
                        candidate_details_id = json_data_candidate['candidateDetails_id']
                        # TODO JOB DESCRIPTION ID
                        candidate_raw_data = json_data_candidate['jsonData']
                        candidate_raw_data_parsing_jd_vs_cv,processed_date = JDvsCVAIBasedCompare().parsed_ai_jd_vs_cv_data(jd_json_data=job_description_json_data,
                                                                                  candidate_raw_json_data=candidate_raw_data)
                        if candidate_raw_data_parsing_jd_vs_cv:
                            # TODO Clean_flag = True
                            clean_flag = True
                            payload = {'positionId':job_description_id,
                                       'candidateId':candidate_details_id,
                                       'comparedOn':processed_date,
                                       'comparisonDetailsJdVsCv':candidate_raw_data_parsing_jd_vs_cv}
                            # TODO --- STEP 3. AFTER MATCHING THE JSON DATA STORED IN RAW DATA INTO JDvsCV TABLES....
                            response = self.hrms_api_service.insert_raw_data_of_JDvsCV_Comparison(hrms_api_service=self.headers,
                                                                                       payload=payload)
                            if response:
                                print("Data successfully Insert into Database")
                            else:
                                print("Data not insert into the Database")
                        else:
                            clean_flag = False
                    else:
                        continue
        except Exception as e:
            print("Exception comes on json candidate details ",str(e))

# TODO --- STEP 4. INSERT THE DATA INTO CANDIDATE OR MAY BE ID OF THE DATA....


"""x = JDvsCVMatchingService(X_TenantID='redberyltech')._read_json_candidate_details()
print(x)"""