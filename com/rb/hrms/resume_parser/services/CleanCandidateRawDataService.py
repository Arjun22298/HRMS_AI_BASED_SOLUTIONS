import logging
import re
from com.rb.hrms.resume_parser.services.MobileService import MobileService
from com.rb.hrms.resume_parser.services.CityService import CityService
from com.rb.hrms.resume_parser.constants.Constants import *
from com.rb.hrms.resume_parser.services.QualificationService import QualificationService
from com.rb.hrms.resume_parser.services.CandidateDataEmailIDService import CandidateDataEmailIDService


class CleanCandidateRawDataService:
    def extract_city_names(self, city_name):
        matches = re.findall(CITY_PATTERN, city_name)
        if matches:
            result = ', '.join(matches)
            return result
        else:
            return city_name

    def filter_qualification_name(self, qualification_name):
        match = re.search(QUALIFICATION_PATTERN, qualification_name)
        if match:
            qualification_name = match.group(0)
            logging.info("Qualification name extracted: %s", qualification_name)
            return qualification_name
        else:
            logging.warning("No qualification name found in the provided string: %s", qualification_name)
            return ""

    def _validate_email(self, cleaned_email):
        # Apply a simple regex pattern for basic email validation
        email_pattern = re.compile(EMAIL_ID_PATTERN)

        if email_pattern.match(cleaned_email):
            return cleaned_email
        else:
            logging.warning(f"Invalid email format: {cleaned_email}")
            return None

    def cleanCandidateRawData(self, hrms_api_service, response):
        try:
            candidate_data = response
            cleaned_city_id = candidate_data.get('cleanedCityId')
            # TODO CLEANING THE CITY COLUMNS
            candidate_city_name = candidate_data.get('city')
            clean_flag = True
            if cleaned_city_id is None:
                if candidate_city_name is not None and isinstance(candidate_city_name, str):
                    candidate_city_upper = candidate_city_name.upper()
                    city_name = self.extract_city_names(candidate_city_upper)
                    cityService = CityService()
                    response = cityService.cleanData(hrms_api_service, city_name)
                    if response is None:
                        clean_flag = False
                    candidate_data['cleanedCityId'] = response

                else:
                    clean_flag = False

            else:
                print('cleanedCityId is already available and no need to reprocess is None')
                pass

            # Clean
            if candidate_data.get('cleanedQualificationId') is None:
                # TODO CLEANING THE QUALIFICATION IN THE RAW DATA TABLES
                candidate_qualification_name = candidate_data.get('higherQualification')
                if candidate_qualification_name is not None:
                    qualification_name = self.filter_qualification_name(candidate_qualification_name)
                    qualification_service = QualificationService()
                    response = qualification_service._ai_cleaning_qualification_name(hrms_api_service,
                                                                                     qualification_name)
                    # TODO ---> INSERT THE DATA INTO  cleanedQualificationId IN THE CANDIDATE DATA
                    # TODO ---> RETURN THE VALUE OF AFTER UPDATE THE RECORD IN THE CANDIDATE DATA
                    if response is None:
                        clean_flag = False

                    candidate_data['cleanedQualificationId'] = response

                else:
                    clean_flag = False
            else:
                print('cleaned Qualification Id is already available and no need to reprocess is None')
            if candidate_data.get('cleanedContactNo') is None:
                # TODO --> PHONE NUMBER SERVICE
                candidate_phone_number = candidate_data.get('phoneNumber')
                if candidate_phone_number is not None:
                    mobileService = MobileService()
                    # TODO --> CLEANING THE MOBILE NUMBER OF CANDIDATE DATA
                    response = mobileService.cleanMobileData(candidate_phone_number)
                    if response is None:
                        clean_flag = False
                    # TODO --> INSERT THE DATA INTO CANDIDATE TABLE AFTER CLEANING PROCESSING DONE  PHONE NUMBER
                    candidate_data['cleanedContactNo'] = response
                else:
                    clean_flag = False
            else:
                print('cleaned Mobile number is already clean and no need to reprocess is None')

            # TODO --> CLEANING THE CANDIDATE EMAIL ID
            candidate_email_id = candidate_data.get('email')
            if candidate_email_id is not None:
                cleaning_candidate_email = CandidateDataEmailIDService()
                clean_email_id = cleaning_candidate_email.cleaningCandidateEmailData(candidate_email_id)
                if clean_email_id is None:
                    clean_flag = False
                    # TODO ---> RETURN THE VALUE OF AFTER UPDATE THE RECORD IN THE CANDIDATE DATA
                    # TODO --> PHONE NUMBER SERVICE
                candidate_data['email'] = clean_email_id
            else:
                print('cleaned email id is already clean and no need to reprocess is None')
            return candidate_data,clean_flag

            # TODO  UPDATE CANDIDATE RAW DATA AND ALSO UPDATE THE DATA INTO CANDIDATE DETAILS
        except:
            hrms_api_service.logout()


