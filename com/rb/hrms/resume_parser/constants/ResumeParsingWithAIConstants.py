API_KEY = 'AIzaSyCJ1lilxDln2C1Eil-0VSfwSFUAo4F6YHY'

PROMPT_TO_GET_INITIAL_DATA = '''I want to extract the Resume or cv  following information from the dataset: candidateName 
dateOfBirth (If available , otherwise Null) gender (If available, otherwise Null) address (If available, 
otherwise Null) linkedUrl (If available,otherwise Null) email (If available, otherwise Null) phoneNumber (If 
available, otherwise Null) higherQualification (If available given only One higherQualification,otherwise Null) 
passingYear(If available ,otherwise Null)
skills ( Please provide individual skills as comma-separated values) 
city (If available,otherwise Null) certification (Please provide individual certification as comma-separated values) 
jobRoleAndResponsibilities(If available,otherwise Null), 
previousCompanyInformation(If available Given Proper_Structure Format (Company_Name,From,To,Duration,
jobRoleAndResponsibilities And Project_Name) otherwise Null) ,
lastCompany (If available (Company_Name),otherwise Null),currentCompanyName (If available, otherwise Null)
And totalNumberOfYearExperience (If available please present them as integers,otherwise Null),
And achievements( If available command-separated value, otherwise Null) Add Another  key  status (Success) if extraction completed. 
The output should be in Exactly_Json_Format.And If Any Reason Resume Should we Not Extract Then
Add one key status and insert the Failed And all value given the null always'''

DESTINATION_FOLDER = r'D:\HrAtomation\final_extracted_pdf_path'

PROMPT_TO_GET_DATA_IN_JSON_FORMAT = """"
{
 "candidateName": "candidateName",
 "dateOfBirth": "dateOfBirth",
 "gender":"gender",
 "address": "address",
 "linkedUrl":"linkedUrl",
 "email": "email",
 "phoneNumber": "phoneNumber",
 "higherQualification": "higherQualification", 
 "passingYear":"passingYear",                   
 "skills": "skills",
 "city": "city",
 "certification": "certification",
 "previousCompanyInformation": "previousCompanyInformation",
 "currentCompanyName": "currentCompanyName",
 "totalNumberOfYearExperience": "totalNumberOfYearExperience", 
 "jobRoleAndResponsibilities":"jobRoleAndResponsibilities",
 "achievements" :"achievements",                                
 "lastCompany":"lastCompany",
 "status":"status"
},Next Json"""

DESTINATION_FOLDER_PATH = r'D:\HrAtomation\final_extracted_pdf_path/*.pdf'

questions2 = '''I want to extract the Resume or cv  following information from the dataset: candidateName 
dateOfBirth (If available , otherwise Null) gender (If available, otherwise Null) address (If available, 
otherwise Null) linkedUrl (If available,otherwise Null) email (If available, otherwise Null) phoneNumber (If 
available, otherwise Null) higherQualification (If available given only One higherQualification,otherwise Null) 
passingYear(If available ,otherwise Null)
skills ( Please provide individual skills as comma-separated values) 
city (If available,otherwise Null) certification (Please provide individual certification as comma-separated values) 
jobRoleAndResponsibilities(If available,otherwise Null), 
previousCompanyInformation(If available Given Proper_Structure Format (Company_Name,From,To,Duration,
jobRoleAndResponsibilities And Project_Name) otherwise Null) ,
lastCompany (If available (Company_Name),otherwise Null),currentCompanyName (If available, otherwise Null)
And totalNumberOfYearExperience (If available please present them as integers,otherwise Null),
And achievements( If available command-separated value, otherwise Null) Add Another  key  status (Success) if extraction completed. 
The output should be in Exactly_Json_Format.And If Any Reason Resume Should we Not Extract Then
Add one key status and insert the Failed And all value given the null always'''

Question_Fourth = """and based on that, provide me with data from data_resumes that fulfills "
                        f" the requirements of the job description Additionally, identify and add a key, 'Matching_Skills_In_The_Both,"
                        f" for skills in both the job description and the resume that match"""

Question_Third = """"
{
 "candidateName": "candidateName",
 "dateOfBirth": "dateOfBirth",
 "gender":"gender",
 "address": "address",
 "linkedUrl":"linkedUrl",
 "email": "email",
 "phoneNumber": "phoneNumber",
 "higherQualification": "higherQualification", 
 "passingYear":"passingYear",                   
 "skills": "skills",
 "city": "city",
 "certification": "certification",
 "previousCompanyInformation": "previousCompanyInformation",
 "currentCompanyName": "currentCompanyName",
 "totalNumberOfYearExperience": "totalNumberOfYearExperience", 
 "jobRoleAndResponsibilities":"jobRoleAndResponsibilities",
 "achievements" :"achievements",                                
 "lastCompany":"lastCompany",
 "status":"status"
},Next Json"""





SOURCE_RESUME_FOLDER = r'D:\HrAtomation\process_data_file'

"""DESTINATION_FOLDER_SUCCESS = r'D:\HrAtomation\final_extracted_pdf_path'

DESTINATION_FOLDER_FAILED = r'D:\HrAtomation\failed_parsing_resume'"""




API_TOKEN = '''eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJyZWRiZXJ5bHRlY2gxMjM0IiwiaWF0IjoxNzA4NDkxOTYxLCJleHAiOjE3MDg1MzUxNjF9.V_EW_O8WAhJfiAOrZeNYWXSp8qAKo1yTkM5cKx-noIvmFk_8SQ1lo8zHupzoqIIJWaquBE-RkEytBbCEoFpleg'''
