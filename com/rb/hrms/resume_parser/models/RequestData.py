from pydantic import BaseModel


class RequestData(BaseModel):
    email_account_name: str
    email_folders_to_scan: str
    email_pickle_path: str
    search_query_tokens: str
    email_token_path: str
    download_resume_folder: str
    email_specific_date_flag: str
    email_specific_date: str
