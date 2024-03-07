from fastapi import HTTPException
from fastapi.responses import JSONResponse


class HRMSApiException:

    @staticmethod
    def generate_resume_parsing_exception(response):
        if response:
            return JSONResponse(content=response, status_code=201)

    @staticmethod
    def insert_data_in_database(json):
        return JSONResponse(content=json, status_code=201)
