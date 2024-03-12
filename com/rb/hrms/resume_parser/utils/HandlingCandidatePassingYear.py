import re
from datetime import datetime


class HandlingCandidatePassingYear:

    def extract_year(self,filter_text):
        # TODO --- MATCHED IF EXPRESSION OF MATCHED IF  AVAILABLE IN YEAR DATA FILTER IT
        year_pattern = r'\b\d{4}\b'
        # TODO -- EXPRESSION THE REGULAR EXPRESSION OF MATCH YEARS OF RANGE IF AVAILABLE IN YEAR DATA FILTER IT

        year_range_pattern = r'(\b\d{4}\b)\s*-\s*(\b\d{4}\b)'

        # TODO --- MATCHED IF THE RANGE WORDS ARE  AVAILABLE IN YEAR DATA FILTER IT
        quarter_semester_pattern = r'Q[1-4]|Fall|Winter|Spring|Summer'

        # TODO --- MATCHED IF FALL/WINTER/SPRING/SUMMER WORDS  AVAILABLE IN YEAR DATA FILETER IT
        season_pattern = r'Fall|Winter|Spring|Summer'

        # TODO --- MATCHED IF PRESENT NAME ARE AVAILABLE IN YEAR DATA
        current_year = datetime.now().year

        # TODO --- MATCHED YEAR
        match = re.search(year_pattern, filter_text)
        if match:
            return int(match.group())
        # TODO --- MATCHED IF YEAR RANGE AVAILABLE IN YEAR DATA FILTER
        match = re.search(year_range_pattern, filter_text)
        if match:
            start_year = int(match.group(1))
            end_year = int(match.group(2))
            if 'Present' in filter_text and end_year == current_year:
                return start_year
            else:
                return end_year
        # TODO --- MATCHED IF QUARTER /SEMESTER AVAILABLE IN YEAR DATA FILTER
        match = re.search(r'(' + quarter_semester_pattern + r')\s*(\d{4})', filter_text)
        if match:
            return int(match.group(2))

        match = re.search(season_pattern + r'\s*(\d{4})', filter_text)
        if match:
            return int(match.group(1))

        # TODO --- MATCHED IF PRESENT WORDS ARE AVAILABLE IN YEAR DATA FILTER IT
        if 'Present' in filter_text:
            return current_year

        return None

