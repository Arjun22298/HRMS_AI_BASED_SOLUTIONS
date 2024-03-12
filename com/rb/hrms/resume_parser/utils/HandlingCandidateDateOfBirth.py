from datetime import datetime


class HandlingCandidateDateOfBirth:
    def convert_birth_date_format(self, date_str):
        if date_str.lower() == "dateofbirth" or date_str.lower() == "null":
            return None

        # TODO -- List of formats to try parsing the date string
        formats_to_try = [
            "%d/%m/%Y",  # TODO--  DD/MM/YYYY
            "%m/%d/%Y",  # TODO-- MM/DD/YYYY
            "%Y/%m/%d",  # TODO -- YYYY/MM/DD
            "%b %d, %Y",  # TODO -- Abbreviated Month DD, YYYY
            "%B %d, %Y",  # TODO -- Full Month DD, YYYY
        ]

        for fmt in formats_to_try:
            try:
                # TODO --- Attempt to parse the date string using the current format
                date_obj = datetime.strptime(date_str, fmt)
                # TODO -- Format the date object into "YYYY-MM-DD" format and return
                return date_obj.strftime("%Y-%m-%d")
            except ValueError:
                # TODO -- If parsing fails, try the next format
                continue

        # TODO -- If none of the formats match, return None
        return None

