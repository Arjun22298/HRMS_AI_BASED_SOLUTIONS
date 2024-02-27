import logging
import re
class MobileService:

    def cleanMobileData(self,candidate_phone_number):
        try:
            cleaned_number = re.sub(r'[^0-9+]', '', candidate_phone_number)
            if not cleaned_number.startswith('+91'):
                cleaned_number = '+91' + cleaned_number

            return cleaned_number
        except Exception as e:
            logging.warning('No data Found !')