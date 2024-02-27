class CandidateRawDetails:
    def __init__(self, id,candidateName, dateOfBirth=None, gender=None, address=None, linkedUrl=None, email=None, phoneNumber=None,
                 higherQualification=None, passingYear=None, skills=None, city=None, certification=None, jobRoleAndResponsibilities=None,
                 previousCompanyInformation=None, currentCompanyName=None, totalNumberOfYearExperience=None, achievements=None,
                 lastCompany=None, cleanStatus=None, cleandCityId = None,cleanedQualificationId=None,processedDataFolder=None,
                 cleanedAltContactNo=None,cleanedCityId=None, cleanedContactNo = None,jsonData=None, processDate=None,status=None,
                 classification = None,candidateDetails_id=None):
        self.id = id
        self.candidateName = candidateName
        self.dateOfBirth = dateOfBirth
        self.gender = gender
        self.address = address
        self.linkedUrl = linkedUrl
        self.email = email
        self.phoneNumber = phoneNumber
        self.cleanedContactNo = cleanedContactNo
        self.cleanedAltContactNo = cleanedAltContactNo
        self.higherQualification = higherQualification
        self.cleanedQualificationId =cleanedQualificationId
        self.passingYear = passingYear
        self.skills = skills
        self.city = city
        self.cleandCityId =cleandCityId
        self.certification = certification
        self.jobRoleAndResponsibilities = jobRoleAndResponsibilities
        self.previousCompanyInformation = previousCompanyInformation
        self.currentCompanyName = currentCompanyName
        self.totalNumberOfYearExperience = totalNumberOfYearExperience
        self.achievements = achievements
        self.lastCompany = lastCompany
        self.cleanStatus = cleanStatus
        self.status = status
        self.classification= classification
        self.cleanedCityId = cleanedCityId
        self.processedDataFolder = processedDataFolder
        self.jsonData = jsonData
        self.processDate = processDate
        self.candidateDetails_id = candidateDetails_id

    def getCandidateName(self):
        print(self.candidateName)
        return self.candidateName

