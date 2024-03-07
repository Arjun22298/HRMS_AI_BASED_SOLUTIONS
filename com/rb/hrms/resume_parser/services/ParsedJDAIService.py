import logging
from com.rb.hrms.resume_parser.services.QualificationService import QualificationService
from com.rb.hrms.resume_parser.constants.HRMSApiConstants import *
from com.rb.hrms.resume_parser.services.HRMSApiService import HRMSApiService
from com.rb.hrms.resume_parser.logging.Logging_file import custom_logger
from com.rb.hrms.resume_parser.services.CityService import CityService
from com.rb.hrms.resume_parser.services.SkillService import SkillService

logger = custom_logger


class ParsedJDAIService:

    @staticmethod
    @custom_logger.log_around
    def generate_JD_response_based_on_HRMS_API(JD_parse_data):
        try:
            api_caller = HRMSApiService(base_url=API_BASE_URL, username=HRMS_API_USERNAME,
                                        password=HRMS_API_PASSWORD)
            api_caller.login()
            jd_json_details = JD_parse_data['jsonData']
            if jd_json_details:
                # TODO --- HERE WE GET THE QUALIFICATION NAME .. IN THE JD
                required_qualification_name = jd_json_details.get('Qualification_required')
                if required_qualification_name:
                    qualification_list = required_qualification_name.split(',')
                    clean_flag = True
                    search_qualification_data = []
                    for qualification_name in qualification_list:
                        # TODO HERE WE CALL THE Qualification_Required API TO GET THAT QUALIFICATION DETAILS .
                        qualification_service = QualificationService()._ai_cleaning_qualification_name(
                            hrms_api_service=api_caller, qualification_name=qualification_name)
                        if qualification_service:
                            search_qualification_data.append(qualification_service)
                    if search_qualification_data:
                        JD_parse_data['qualifications'] = search_qualification_data
                    else:
                        JD_parse_data['qualifications'] = None
                else:
                    JD_parse_data['qualifications'] = None
                # TODO -- HERE WE GET THE CITY NAME ....  IN THE JD
                required_city_name = jd_json_details.get('city')
                if required_city_name:
                    city_names = required_city_name.split(',')
                    if len(city_names) > 1:
                        clean_flag = True
                        search_city_name = []
                        for city in city_names:
                            # TODO .. HERE WE CALL THE SEARCH CITY NAME API TO GET THAT CITY DETAILS
                            city_service = CityService().cleanData(hrms_api_service=api_caller, city_name=city)
                            if city_service:
                                search_city_name.append(city_service)
                        if search_city_name:
                            JD_parse_data['city'] = search_city_name
                        else:
                            JD_parse_data['city'] = None
                        # print("This is the actual response city of Jd parse data::", JD_parse_data)
                else:
                    JD_parse_data['city'] = None

                # TODO ---HERE WE GET THE SKILLS NAME ... IN THE JD
                required_skill_name = jd_json_details.get('Skills')
                if required_skill_name:
                    skills_names = required_skill_name.split(',')
                    if len(skills_names) > 1:
                        clean_flag = True
                        search_skills_name = []
                        for skill in skills_names:
                            # TODO --- HERE WE CALL THE SKILLS API AND GET THAT DETAILS OF SKILLS.
                            skill_service = SkillService().cleanData(hrms_api_service=api_caller, skill_name=skill)
                            if skill_service:
                                search_skills_name.append(skill_service)
                        if search_skills_name:
                            JD_parse_data['skill'] = search_skills_name
                        else:
                            JD_parse_data['skill'] = None
                else:
                    JD_parse_data['skill'] = None

                # TODO --> WHERE WE INSERT Experience ...
                experience = jd_json_details.get('Experience_Required')
                if experience:
                    JD_parse_data['experience'] = experience
                else:
                    JD_parse_data['experience'] = None

                # TODO --> HERE WE SET THE VALUE OF MUST OF HAVE
                mustToHave = jd_json_details.get('mustToHave')
                if mustToHave:
                    JD_parse_data['mustToHave'] = mustToHave
                else:
                    JD_parse_data['mustToHave'] = None

                # TODO ---> HERE WE SET THE VALUE NICE TO HAVE
                niceToHave = jd_json_details.get('niceToHave')
                if niceToHave:
                    JD_parse_data['niceToHave'] = niceToHave
                else:
                    JD_parse_data['niceToHave'] = None

                # TODO -- HERE WE SET THE VALUE OF JOB LOCATIONS

                jobLocation = jd_json_details.get('jobLocation')
                if jobLocation:
                    JD_parse_data['jobLocation'] = jobLocation
                else:
                    JD_parse_data['jobLocation'] = None

                # TODO -- HERE WE SET THE IRRESPONSIBILITY ...
                roleAndResponsibility = jd_json_details.get('roleAndResponsibility')
                if roleAndResponsibility:
                    JD_parse_data['roleAndResponsibility'] = roleAndResponsibility
                else:
                    JD_parse_data['roleAndResponsibility'] = None
                # TODO -- HERE WE SET THE SALARY RANGE
                salaryRange = jd_json_details.get('salaryRange')
                if salaryRange:
                    JD_parse_data['salaryRange'] = salaryRange
                else:
                    JD_parse_data['salaryRange'] = None

                # TODO --- HERE SET THE NAME OF JOB ...
                job_title = jd_json_details.get('job_title')
                if job_title:
                    JD_parse_data['name'] = job_title
                else:
                    JD_parse_data['name'] = None
            print("This is the actual response city of Jd parse data::", JD_parse_data)

            """required_city_name = jd_json_details.get('city')
            city_names = required_city_name.split(',')
            if len(city_names) > 1:
                clean_flag = True
                search_city_name = []
                for city in city_names:
                    # TODO .. HERE WE CALL THE SEARCH CITY NAME API TO GET THAT CITY DETAILS
                    city_service = CityService().cleanData(hrms_api_service=api_caller, city_name=city)
                    if city_service:
                        search_city_name.append(city_service)
                if search_city_name:
                    JD_parse_data['city'] = search_city_name
                else:
                    JD_parse_data['city'] = None
                print("This is the actual response city of Jd parse data::", JD_parse_data)
            else:
                clean_flag = False
                # TODO --- HERE WE CALL THE SKILLS API AND GET THAT DETAILS OF SKILLS."""

            else:
                return None
            """response = hrms_api_service.hrms_api_call(headers=api_caller.get_headers(), method='POST',
                                                url=api_caller.base_url + INSERT_JD_PARSED_DETAILS_INTO_DATABASE,
                                                data=JD_parse_data)
            if response:
                return response"""
            api_caller.logout()
        except Exception as e:
            logging.error(str(e), exc_info=True)
