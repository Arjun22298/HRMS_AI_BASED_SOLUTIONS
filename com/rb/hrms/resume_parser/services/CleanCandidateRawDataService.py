import logging
import re
from com.rb.hrms.resume_parser.services.MobileService import MobileService
from com.rb.hrms.resume_parser.services.CityService import CityService
from com.rb.hrms.resume_parser.constants.Constants import *
from com.rb.hrms.resume_parser.services.QualificationService import QualificationService
from com.rb.hrms.resume_parser.services.CandidateDataEmailIDService import CandidateDataEmailIDService
from com.rb.hrms.resume_parser.utils.HandlingCandidatePassingYear import HandlingCandidatePassingYear
from com.rb.hrms.resume_parser.utils.HandlingCandidateDateOfBirth import HandlingCandidateDateOfBirth
from com.rb.hrms.resume_parser.utils.FilterCityName import FilterCityName


class CleanCandidateRawDataService:

    def filter_qualification_name(self, qualification_name):
        match = re.search(QUALIFICATION_PATTERN, qualification_name)
        if match:
            qualification_name = match.group(0)
            logging.info("Qualification name extracted: %s", qualification_name)
            return qualification_name
        else:
            logging.warning("No qualification name found in the provided string: %s", qualification_name)
            return ""

    def filter_experience_data(self, experience_data):
        # Regular expression pattern to match integer values
        integer_pattern = r'\b\d+\b'

        # Match integer
        match = re.search(integer_pattern, experience_data)
        if match:
            return int(match.group())
        else:
            # Handling '10+ years' case
            match = re.search(r'\b(\d+)\s*\+\s*years?\b', experience_data)
            if match:
                return int(match.group(1))

        return None

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

            if cleaned_city_id is None:
                candidate_city_name = candidate_data.get('city')
                if candidate_city_name is not None and isinstance(candidate_city_name, str):
                    clean_flag = True
                    city_name = FilterCityName().clean_city_name(candidate_city_name)
                    cityService = CityService()
                    response = cityService.cleanData(hrms_api_service, city_name)
                    if response is None:
                        clean_flag = False
                candidate_data['cleanedCityId'] = response
            else:
                clean_flag = None

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
                clean_flag = None
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
                clean_flag = None

            # TODO ---> CLEANING THE DATE OF BIRTH
            candidate_date_of_birth = candidate_data.get('dateOfBirth')
            if candidate_date_of_birth is not None:
                clean_flag = True
                # TODO --- FILTER THE DATE OF BIRTH OF CANDIDATE
                candidate_birth_date = HandlingCandidateDateOfBirth().convert_birth_date_format(candidate_date_of_birth)
                if candidate_birth_date is None:
                    clean_flag = False
                candidate_data['dateOfBirth'] = candidate_birth_date
            else:
                clean_flag = None

            # TODO --> CLEANING THE CANDIDATE EMAIL ID
            candidate_email_id = candidate_data.get('email')
            if candidate_email_id is not None:
                clean_flag = True
                cleaning_candidate_email = CandidateDataEmailIDService()
                clean_email_id = cleaning_candidate_email.cleaningCandidateEmailData(candidate_email_id)
                if clean_email_id is None:
                    clean_flag = False
                    # TODO ---> RETURN THE VALUE OF AFTER UPDATE THE RECORD IN THE CANDIDATE DATA
                    # TODO --> PHONE NUMBER SERVICE
                candidate_data['email'] = clean_email_id
            else:
                clean_flag = None

            # TODO CLEANING THE PASSING YEARS ...
            candidate_passing_year = candidate_data.get('passingYear')
            if candidate_passing_year is not None:
                response_candidate_passing_year = HandlingCandidatePassingYear().extract_year(candidate_passing_year)
                if response_candidate_passing_year is None:
                    clean_flag = False
                candidate_data['passingYear'] = response_candidate_passing_year
            else:
                clean_flag = None

            # TODO --- CLEANING THE EXPERIENCE DATA ...
            candidate_experience_data = candidate_data.get('totalNumberOfYearExperience')
            if candidate_experience_data is not None:
                experience_data = self.filter_experience_data(candidate_experience_data)
                if experience_data is None:
                    clean_flag = False
                candidate_data['totalNumberOfYearExperience'] = experience_data
            else:
                clean_flag = False
            return candidate_data, clean_flag

            # TODO  UPDATE CANDIDATE RAW DATA AND ALSO UPDATE THE DATA INTO CANDIDATE DETAILS
        except:
            hrms_api_service.logout()
