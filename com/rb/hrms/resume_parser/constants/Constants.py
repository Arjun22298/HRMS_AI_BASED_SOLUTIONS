API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']
PROCESSED = "D:/hrms-application-parent/HrAtomation/final_extracted_pdf_path"
DOWNLOADS = "D:\HrAtomation\ResumeAiBased"


Resume = """if resume_matched(If resume_matched, otherwise Null) and given proper"""
FORMAT = """
{"resume_matched":"resume_matched",
"file_name":"file_name"},NextJson"""


CITY_PATTERN = r'\b([A-Z][a-zA-Z\s]+)\s*(?=[,|\(|\|])'

QUALIFICATION_PATTERN = r'\b([A-Z][A-Za-z\s\.]+(?:\s[A-Za-z\s\.]+)*)\b'


EMAIL_ID_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'





data =''' {"fullName": "Arjun Raj",
  "email": "arjunraj7579@gmail.com",
  "contactNo": "+918340397950",
  "altContactNo": null,
  "gender": null,
  "birthDate": null,
  "passingYear": "2022",
  "whatsappNo": null,
  "resumeUrl": null,
  "linkedInUrl": "https://www.linkedin.com/in/arjun-raj-072485231/",
  "experienceInYears": null,
  "profileScannedOn": "2024-02-21T00:00:00",
  "currentCompanyName": "RedBeryl Tech Solutions",
  "profileReferance": null,
  "feedbackStatus": null,
  "address": "Pune (Maharashtra)",
  "qualification": {
    "id": 200,
    "name": "M.SC COMPUTER SCIENCE",
    "description": "MASTER OF SCIENCE IN COMPUTER SCIENCE",
    "isActive": true
  },
  "city": {
    "id": 191,
    "cityName": "PUNE",
    "isActive": true
  },
  "skills": "Python, SQL, Groovy, FastAPI, Git, Docker, CICD, Jenkins, Linux, Kafka, Apache Airflow, Apache Spark, DSA, Design Pattern, Google API, Pandas, Data Structure Algorithm",
  "statusId": {
    "id": 1,
    "statusName": "Active",
    "statusType": "Custom Statuses",
    "isActive": true
  }
}'''