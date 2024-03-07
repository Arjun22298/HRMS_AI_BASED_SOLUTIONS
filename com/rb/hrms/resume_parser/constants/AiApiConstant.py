GOOGLE_API_KEY = 'AIzaSyBjIat3csnA4y8Jki8IV7EvPpil23fbxdg'


CITY_DETAILS_PROMPT_PART1 =(f"Give me correct city_name of ")
CITY_DETAILS_PROMPT_PART2 = " by applying spell correction and recent name if it has in the strict json format of "
CITY_DETAILS_RESPONSE_FORMAT = """{city_name:city_name }"""



SEARCH_QUALIFICATION_RESPONSE_JSON = {"name": 'abbreviation', "description": 'descriptive name'}
SEARCH_QUALIFICATION_PROMPT_PART1 = f"give me accurate abbreviation and descriptive name of qualification"
SEARCH_QUALIFICATION_PROMPT_PART2 = f"in the strict json format of"
SEARCH_QUALIFICATION_PROMPT_PART3= f"as a response"


SKILL_DETAILS_PROMPT_PART1 =(f"Give me correct skill_name of ")
SKILL_DETAILS_PROMPT_PART2 = " by applying spell correction and recent name if it has in the strict json format of "
SKILL_DETAILS_RESPONSE_FORMAT = """{skill_name:skill_name }"""
