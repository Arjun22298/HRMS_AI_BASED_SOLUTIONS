class Qualification:
    def __init__(self, id, name, description, isActive):
        self.id = id
        self.name = name
        self.description = description
        self.isActive = isActive


class City:
    def __init__(self, id, cityName, isActive):
        self.id = id
        self.cityName = cityName
        self.isActive = isActive


class Skill:
    def __init__(self, id, skillName, isActive):
        self.id = id
        self.skillName = skillName
        self.isActive = isActive


class StatusId:
    def __init__(self, id, statusName, statusType, isActive):
        self.id = id
        self.statusName = statusName
        self.statusType = statusType
        self.isActive = isActive


class CandidateDetails:
    def __init__(self, fullName, email, contactNo, altContactNo, gender, birthDate, passingYear, whatsappNo, resumeUrl,
                 linkedInUrl,
                 experienceInYears, profileScannedOn, currentCompanyName, profileReferance, feedbackStatus, address,
                 qualification_id, city_id,
                 skills=None, statusId=None):
        self.fullName = fullName
        self.email = email
        self.contactNo = contactNo
        self.altContactNo = altContactNo
        self.gender = gender
        self.birthDate = birthDate
        self.passingYear = passingYear
        self.whatsappNo = whatsappNo
        self.resumeUrl = resumeUrl
        self.linkedInUrl = linkedInUrl
        self.experienceInYears = experienceInYears
        self.profileScannedOn = profileScannedOn
        self.currentCompanyName = currentCompanyName
        self.profileReferance = profileReferance
        self.feedbackStatus = feedbackStatus
        self.address = address
        self.qualification_id = Qualification(**qualification_id)
        self.city_id = City(**city_id)
        self.skills = skills
        self.statusId = statusId

    def getFullName(self):
        print(f"Full Name :: {self.fullName}")
        return self.fullName

    def getSkills(self):
        print(f"Skills Name :: {self.skills}")
        return self.skills
