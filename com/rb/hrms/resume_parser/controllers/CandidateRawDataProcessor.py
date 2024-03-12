import logging
from com.rb.hrms.resume_parser.constants.HRMSApiConstants import *
from com.rb.hrms.resume_parser.services.HRMSApiService import HRMSApiService
from com.rb.hrms.resume_parser.constants.HRMSApiConstants import GET_CANDIDATE_RAW_DETAILS_API_END_POINT
from com.rb.hrms.resume_parser.services.CleanCandidateRawDataService import CleanCandidateRawDataService
from com.rb.hrms.resume_parser.mappers.CandidateMapper import CandidateMapper
from com.rb.hrms.resume_parser.models.CandidateRawDetails import CandidateRawDetails
from com.rb.hrms.resume_parser.services.CandidateDetailsService import CandidateDetailsService
from com.rb.hrms.resume_parser.utils.ConvertNullToNone import ConvertNullToNone


class CandidateRawDataProcessor:
    def __init__(self, Authorization, X_TenantID):
        self.convert_null_object = ConvertNullToNone()
        self.authorization = Authorization
        self.x_tenantid = X_TenantID

    def process_candidate_raw_details(self):
        try:
            api_caller = HRMSApiService(base_url=API_BASE_URL, username=HRMS_API_USERNAME,
                                        password=HRMS_API_PASSWORD, jwt_token_id=self.authorization,
                                        X_TenantID=self.x_tenantid)
            api_caller.login()

            response = api_caller.hrms_api_call(headers=api_caller.get_headers(), method='GET',
                                                url=api_caller.base_url + GET_CANDIDATE_RAW_DETAILS_API_END_POINT)
            # TODO ---> MULTIPLE RECORD FROM RAW DATA
            if response is not None:
                for candidate_data in response:
                    if candidate_data['candidateDetails_id'] is None:
                        service_response = self.convert_null_object.convert_null_to_none(candidate_data)
                        service_response, cleanflag = CleanCandidateRawDataService().cleanCandidateRawData(
                            hrms_api_service=api_caller,
                            response=service_response)
                        print("This is the clean flag response! ", cleanflag)
                        #service_response = self.convert_null_object.convert_null_to_none(service_response)

                        clean_city_id = service_response.get('cleanedCityId')
                        clean_qualification_id = service_response.get('cleanedQualificationId')

                        if service_response:
                            # TODO INSERT CANDIDATE DETAILS AND UPDATE CANDIDATE RAW DETAILS
                            if (not isinstance(clean_city_id, int) and 'id' in clean_city_id) and (
                                    not isinstance(clean_qualification_id, int) and 'id' in clean_qualification_id):
                                candidate_details = CandidateMapper().map(CandidateRawDetails(**service_response))
                                # TODO ---> HERE WE CONVERT 'NULL' STRING TO NONE FORMAT . . .
                                response_of_candidate = CandidateDetailsService().insert_into_candidate_details(
                                    hrms_api_service=api_caller, payload=candidate_details)
                                print("Insert data into candidate details tables", response_of_candidate)

                                service_response['cleanedCityId'] = clean_city_id.get('id')
                                service_response['cleanedQualificationId'] = clean_qualification_id.get('id')

                                if response_of_candidate is not None:
                                    # TODO - set id valus to CandidateRawDetails id - Field needs to be added in the candidate_data_Details table for foriegn key relation
                                    # service_response.
                                    # TODO - set clean_status = flag received as parameter - true
                                    service_response['candidateDetails_id'] = response_of_candidate.get('id')
                                    service_response['cleanStatus'] = True
                                    # TODO - update Candidate Raw Details
                                    raw_details_response = CandidateDetailsService().update_into_raw_candidate_tables(
                                        hrms_api_service=api_caller,
                                        payload=service_response,
                                        id=service_response.get('id'))
                                    if raw_details_response is None:
                                        print(f"Update Candidate Raw Details Failed...")
                                    else:
                                        print(f"Update Candidate Raw Details Successful...")
                                else:
                                    # TODO UPDATE THE CANDIDATE RAW DETAILS
                                    # TODO - set clean_status = flag received as parameter - true
                                    # TODO -- HERE WE CHECK THE CLEAN STATUS
                                    if service_response['cleanStatus'] is not None:
                                        raw_details_response = CandidateDetailsService().update_into_raw_candidate_tables(
                                            hrms_api_service=api_caller,
                                            payload=service_response,
                                            id=service_response.get('id'))
                                    else:
                                        service_response['cleanStatus'] = False
                                        raw_details_response = CandidateDetailsService().update_into_raw_candidate_tables(
                                            hrms_api_service=api_caller,
                                            payload=service_response,
                                            id=service_response.get('id'))

                                # print("This is the raw details response ", raw_details_response)
                                if raw_details_response is None:
                                    print(f"Update Candidate Raw Details Failed...")
                                else:
                                    print(f"Update Candidate Raw Details Successful...")
                            else:
                                # TODO UPDATE THE CANDIDATE RAW DETAILS
                                # TODO - set clean_status = flag received as parameter - true
                                if service_response['cleanStatus'] is not None:
                                    continue
                                else:
                                    if clean_city_id:
                                        clean_city_id.get('id')
                                    service_response['cleanedCityId'] = clean_city_id
                                    if clean_qualification_id:
                                        clean_qualification_id.get('id')
                                    service_response['cleanedQualificationId'] = clean_qualification_id
                                    service_response['cleanStatus'] = False
                                    raw_details_response = CandidateDetailsService().update_into_raw_candidate_tables(
                                        hrms_api_service=api_caller,
                                        payload=service_response,
                                        id=service_response.get('id'))
                            if raw_details_response is None:
                                print("Update Candidate Raw Details Failed....")
                            else:
                                response = {"candidate_raw_id": raw_details_response['id'],
                                            "candidate_raw_clean_status": raw_details_response['cleanStatus'],
                                            "candidateDetails_id": raw_details_response['candidateDetails_id']
                                            }
                        else:
                            return None
                    else:
                        continue
                return response
        except Exception as e:
            logging.error(str(e), exc_info=True)
            return None
        finally:
            api_caller.logout()


"""Candidate_Data_Details = (CandidateRawDataProcessor(Authorization=None, X_TenantID='redberyltech')
                          .process_candidate_raw_details())
print(Candidate_Data_Details)"""
