from fastapi import HTTPException
from fastapi.responses import JSONResponse


class HRMSApiException:

    @staticmethod
    def generate_resume_parsing_valid_exception(response):
        if response:
            return JSONResponse(content=response, status_code=201)

    @staticmethod
    def generate_resume_parsing_invalid_exception(response):
        if response:
            return JSONResponse(content=response, status_code=201)

    @staticmethod
    def insert_data_in_database(json):
        return JSONResponse(content=json, status_code=201)

    @staticmethod
    def valid_parse_jd_response(json_response):
        return JSONResponse(content=json_response, status_code=201)

    @staticmethod
    def invalid_jd_response(json_response):
        return JSONResponse(content=json_response, status_code=404)

    @staticmethod
    def valid_clean_resume_data_response(json_response):
        return JSONResponse(content=json_response, status_code=201)

    @staticmethod
    def invalid_clean_resume_data_response(json_response):
        return JSONResponse(content=json_response, status_code=404)

    @staticmethod
    def invalid_resume_data_parsing_response(json_response):
        return JSONResponse(content=json_response,status_code=404)

    @staticmethod
    def valid_resume_data_parsing_response(json_response):
        return JSONResponse(content=json_response,status_code=201)
