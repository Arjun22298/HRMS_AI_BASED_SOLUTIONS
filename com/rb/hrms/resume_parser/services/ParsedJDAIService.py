import logging
from com.rb.hrms.resume_parser.services.QualificationService import QualificationService
from com.rb.hrms.resume_parser.constants.HRMSApiConstants import *
from com.rb.hrms.resume_parser.logging.Logging_file import custom_logger
from com.rb.hrms.resume_parser.services.CityService import CityService
from com.rb.hrms.resume_parser.services.SkillService import SkillService

logger = custom_logger


class ParsedJDAIService:
    @custom_logger.log_around
    def generate_JD_response_based_on_HRMS_API(self, hrms_api_service, JD_parse_data):
        try:
            # TODO HERE WE CALL THE INSERT INTO RAW DETAILS ON JOB DESCRIPTION TABLES....
            url = f"{hrms_api_service.base_url}/{INSERT_JOB_DESCRIPTION_RAW_DETAILS_API_END_POINT}"
            response = hrms_api_service.hrms_api_call(headers=hrms_api_service.headers, method='POST',
                                                      url=url, data=JD_parse_data)
            if response:
                print("Insert data into raw data details Successfully Done !")
            else:
                print("Raw Data Details Insert Failed !")

            jd_json_details = JD_parse_data['jsonData']
            if jd_json_details:
                # TODO --- HERE WE GET THE QUALIFICATION NAME .. IN THE JD
                required_qualification_name = jd_json_details.get('Qualification_required')
                if required_qualification_name:
                    qualification_list = required_qualification_name.split(',')

                    search_qualification_data = []
                    for qualification_name in qualification_list:
                        # TODO HERE WE CALL THE Qualification_Required API TO GET THAT QUALIFICATION DETAILS .
                        qualification_service = QualificationService()._ai_cleaning_qualification_name(
                            hrms_api_service=hrms_api_service, qualification_name=qualification_name)
                        if qualification_service:
                            search_qualification_data.append(qualification_service)
                    if search_qualification_data:
                        clean_flag = True
                        JD_parse_data['qualifications'] = search_qualification_data
                    else:

                        JD_parse_data['qualifications'] = None
                else:
                    clean_flag = False
                    JD_parse_data['qualifications'] = None
                # TODO -- HERE WE GET THE CITY NAME ....  IN THE JD
                required_city_name = jd_json_details.get('city')
                if required_city_name:
                    city_names = required_city_name.split(',')
                    if len(city_names) > 1:

                        search_city_name = []
                        for city in city_names:
                            # TODO .. HERE WE CALL THE SEARCH CITY NAME API TO GET THAT CITY DETAILS
                            city_service = CityService().cleanData(hrms_api_service=hrms_api_service, city_name=city)
                            if city_service:
                                search_city_name.append(city_service)
                        if search_city_name:
                            clean_flag = True
                            JD_parse_data['city'] = search_city_name
                        else:
                            JD_parse_data['city'] = None

                else:
                    clean_flag = False
                    JD_parse_data['city'] = None

                # TODO ---HERE WE GET THE SKILLS NAME ... IN THE JD
                required_skill_name = jd_json_details.get('Skills')
                if required_skill_name:
                    skills_names = required_skill_name.split(',')
                    if len(skills_names) > 1:

                        search_skills_name = []
                        for skill in skills_names:
                            # TODO --- HERE WE CALL THE SKILLS API AND GET THAT DETAILS OF SKILLS.
                            skill_service = SkillService().cleanData(hrms_api_service=hrms_api_service,
                                                                     skill_name=skill)
                            if skill_service:
                                search_skills_name.append(skill_service)
                        if search_skills_name:
                            clean_flag = True
                            JD_parse_data['skill'] = search_skills_name
                        else:
                            JD_parse_data['skill'] = None
                else:
                    clean_flag = False
                    JD_parse_data['skill'] = None

                # TODO --> WHERE WE INSERT Experience ...
                experience = jd_json_details.get('Experience_Required')
                if experience:
                    clean_flag = True
                    JD_parse_data['experience'] = experience
                else:
                    clean_flag = False
                    JD_parse_data['experience'] = None

                # TODO --> HERE WE SET THE VALUE OF MUST OF HAVE
                mustToHave = jd_json_details.get('mustToHave')
                if mustToHave:
                    clean_flag = True
                    JD_parse_data['mustToHave'] = mustToHave
                else:
                    clean_flag = False
                    JD_parse_data['mustToHave'] = None

                # TODO ---> HERE WE SET THE VALUE NICE TO HAVE
                niceToHave = jd_json_details.get('niceToHave')
                if niceToHave:
                    clean_flag = True
                    JD_parse_data['niceToHave'] = niceToHave
                else:
                    clean_flag = False
                    JD_parse_data['niceToHave'] = None

                # TODO -- HERE WE SET THE VALUE OF JOB LOCATIONS

                jobLocation = jd_json_details.get('jobLocation')
                if jobLocation:
                    clean_flag = True
                    JD_parse_data['jobLocation'] = jobLocation
                else:
                    clean_flag = False
                    JD_parse_data['jobLocation'] = None

                # TODO -- HERE WE SET THE IRRESPONSIBILITY ...
                roleAndResponsibility = jd_json_details.get('roleAndResponsibility')
                if roleAndResponsibility:
                    clean_flag = True
                    JD_parse_data['roleAndResponsibility'] = roleAndResponsibility
                else:
                    clean_flag = False
                    JD_parse_data['roleAndResponsibility'] = None
                # TODO -- HERE WE SET THE SALARY RANGE
                salaryRange = jd_json_details.get('salaryRange')
                if salaryRange:
                    clean_flag = True
                    JD_parse_data['salaryRange'] = salaryRange
                else:
                    clean_flag = False
                    JD_parse_data['salaryRange'] = None

                # TODO --- HERE SET THE NAME OF JOB ...
                job_title = jd_json_details.get('job_title')
                if job_title:
                    clean_flag = True
                    JD_parse_data['name'] = job_title
                else:
                    clean_flag = False
                    JD_parse_data['name'] = None
                # TODO ---- HERE WE SET THE NULL VALUE OF benefits_and_perks
                JD_parse_data['benefits_and_perks'] = None

                JD_parse_data['jobType'] = None

                JD_parse_data['shifts'] = None

                JD_parse_data['languages'] = None

                JD_parse_data['skillRequired'] = None

            if JD_parse_data:
                del JD_parse_data['date']
                response = self.insert_data_into_job_description_Table(hrms_api_service=hrms_api_service,
                                                                       jd_response_data=JD_parse_data)
                # TODO HERE WE CALL THE PUT API TO INSERT THE DATA INTO THE JD DESCRIPTION TABLE
                if response:
                    clean_flag = True
                else:
                    clean_flag = False
            else:
                clean_flag = False
                # TODO HERE WE DON'T INSERT THE DATA INTO THE JD DESCRIPTION TABLE IF CLEAN FLAG BECOME FALSE
            return response, clean_flag
        except Exception as e:
            logging.error(str(e), exc_info=True)

    @custom_logger.log_around
    def insert_data_into_job_description_Table(self, hrms_api_service, jd_response_data):
        url = f"{hrms_api_service.base_url}/{INSERT_JOB_DESCRIPTION_DETAILS_API_END_POINT}"
        response = hrms_api_service.hrms_api_call(headers=hrms_api_service.headers, method='POST',
                                                  url=url, data=jd_response_data)
        if response:
            print("Result Response ::", response)
            return response
        else:
            return None
