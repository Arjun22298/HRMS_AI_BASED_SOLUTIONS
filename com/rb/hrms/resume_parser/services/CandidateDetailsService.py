import json
from com.rb.hrms.resume_parser.constants.HRMSApiConstants import INSERT_CANDIDATE_DETAILS_API_END_POINT, \
    PUT_CANDIDATE_RAW_DETAILS_API_END_POINT
from com.rb.hrms.resume_parser.constants.Constants import *
import logging


class CandidateDetailsService:
    @staticmethod
    def insert_into_candidate_details(hrms_api_service, payload):
        try:

            url = f"{hrms_api_service.base_url}/{INSERT_CANDIDATE_DETAILS_API_END_POINT}"
            print(f"URL :: {url}")
            print(f"PAYLOAD :: {payload}")
            response = hrms_api_service.hrms_api_call(headers=hrms_api_service.headers, method='POST',
                                                      url=url, data=payload)
            return response
        except Exception as e:
            logging.error(str(e), exc_info=True)
            return None

    @staticmethod
    def update_into_raw_candidate_tables(hrms_api_service, payload, id):
        try:

            url = f"{hrms_api_service.base_url}/{PUT_CANDIDATE_RAW_DETAILS_API_END_POINT}"
            print(f"URL :: {url}")
            response = hrms_api_service.hrms_api_call(headers=hrms_api_service.headers, method='PUT',
                                                      url=url.format(id=id), data=payload)
            return response
        except Exception as e:
            logging.error(str(e), exc_info=True)
            return None
