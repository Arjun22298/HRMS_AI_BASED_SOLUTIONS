from datetime import datetime


class HandlingCandidateDateOfBirth:
    @staticmethod
    def convert_birth_date_format(date_str):
        if not date_str.strip():  # TODO -- Check if date_str is empty or contains only whitespace
            return None

        # TODO List of formats to try parsing the date string
        formats_to_try = [
            "%d-%m-%Y",  # DD-MM-YYYY
            "%Y-%m-%d",  # YYYY-MM-DD
            "%d %b %Y",  # DD Abbreviated Month YYYY (e.g., 05 Nov 1997)
            "%b-%d-%Y",  # Abbreviated Month-DD-YYYY (e.g., Nov-12-2000)
            "%b %d %Y",  # Abbreviated Month DD YYYY (e.g., NOV 17 2000)
            "%b %d, %Y",  # Abbreviated Month DD, YYYY (e.g., Jun 15, 1990)
            "%B%d,%Y",  # Full MonthDD,YYYY (e.g., April28,2000)
            "%B %d, %Y",  # Full Month DD, YYYY (e.g., June 15, 1990)
            "%Y/%m/%d",  # YYYY/MM/DD
            "%m/%d/%Y",  # MM/DD/YYYY
            "%d/%m/%Y",  # DD/MM/YYYY
        ]

        date_str = date_str.strip()  # TODO -- Remove leading and trailing whitespace

        for fmt in formats_to_try:
            try:
                # TODO -- Attempt to parse the date string using the current format
                date_obj = datetime.strptime(date_str, fmt)
                # TODO -- Format the date object into "YYYY-MM-DD" format and return
                return date_obj.strftime("%Y-%m-%d")
            except ValueError:
                # TODO -- If parsing fails, try the next format
                continue

        # TODO -- If none of the formats match, return None
        return None
