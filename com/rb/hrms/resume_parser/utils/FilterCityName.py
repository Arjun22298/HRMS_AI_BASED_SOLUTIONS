import re


class FilterCityName:
    @staticmethod
    def clean_city_name(city_name):
        # TODO - Remove any leading or trailing whitespace
        city_name = city_name.strip()

        # TODO -Replace hyphens with spaces
        city_name = city_name.replace("-", " ")

        # TODO Remove underscores
        city_name = city_name.replace("_", "")

        # TODO Remove commas and anything after commas
        city_name = city_name.split(",")[0]

        # TODO Remove parentheses and anything inside parentheses
        city_name = re.sub(r'\([^)]*\)', '', city_name)

        # TODO Remove periods at the end of the string
        city_name = city_name.rstrip(".")

        #TODO  Remove apostrophes
        city_name = city_name.replace("'", "")

        # TODO Remove any non-alphanumeric characters except spaces
        city_name = re.sub(r'[^a-zA-Z\s]', '', city_name)

        # TODO Capitalize each word in the city name
        city_name = city_name.title()
        return city_name.upper()
