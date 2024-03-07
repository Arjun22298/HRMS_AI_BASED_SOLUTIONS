import re
import logging
from com.rb.hrms.resume_parser.constants.Constants import *


class CandidateDataEmailIDService:
    def cleaningCandidateEmailData(self, cleaned_email):
        # Apply a simple regex pattern for basic email validation
        email_pattern = re.compile(EMAIL_ID_PATTERN)
        if email_pattern.match(cleaned_email):
            return cleaned_email
        else:
            logging.warning(f"Invalid email format: {cleaned_email}")
            return None
