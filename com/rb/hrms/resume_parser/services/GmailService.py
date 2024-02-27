import time
# from Email_process.constants import API_NAME, API_VERSION, SCOPES
import os
import pickle
from datetime import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
from email import message_from_string
from googleapiclient.discovery import build
from com.rb.hrms.resume_parser.services.EmailService import EmailService
from com.rb.hrms.resume_parser.logging.RollingFileLogger import RollingFileLogger
import logging
from com.rb.hrms.resume_parser.constants.Constants import *
from com.rb.hrms.resume_parser.utils.EmailContentExtractor import EmailContentExtractor
from com.rb.hrms.resume_parser.utils.QueryBuilder import QueryBuilder
from typing import List


class GmailService(EmailService):

    def __init__(self):
        self.logger = RollingFileLogger("../../../../../logs/ResumeParser.log")

    def process(self, request_data):
        try:
            self.service = self.connect(request_data)
        except Exception as e:
            print("Excepting in Connection....")
        try:
            search_query = QueryBuilder().build_query(request_data)
            print("This is the query sytring",search_query)
        except Exception as e:
            print("Exception in Query Builder...")
        try:
            filtered_email_messages = self.get_emails(search_query)
        except Exception as e:
            print("Exception in Extracting Emails...")
        try:
            self.download_attachment(request_data.download_resume_folder, filtered_email_messages)
        except Exception as e:
            print("Exception in Downloading Attachments...")

    def connect(self, request_data):
        if request_data is None:
            # TODO - Throw connection exception
            return
        else:
            self.client_secret_file = request_data.email_pickle_path
            logging.info(f"This is the CLIENT FILE CREDENTIALS:- {self.client_secret_file}")
            self.pickle_path = request_data.email_pickle_path
            logging.info(f"This is the pickle File Credentials: {self.pickle_path}")
            self.service = self.__create_service(self.client_secret_file, self.pickle_path, API_NAME, API_VERSION,
                                                 SCOPES)
            # self.response = HandlingQueryString(params).build_query()
        return self.service

    def __create_service(self, client_secret_file, pickle_path, api_name, api_version, *scopes):
        EMAIL_CREDENTIALS = pickle_path
        CLIENT_SECRET_FILE = client_secret_file
        API_SERVICE_NAME = api_name
        API_VERSION = api_version
        SCOPES = [scope for scope in scopes[0]]

        cred = None
        working_dir = EMAIL_CREDENTIALS
        token_dir = 'token files'
        prefix = ''
        pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}{prefix}.pickle'

        # Check if token dir exists first, if not, create the folder
        if not os.path.exists(os.path.join(working_dir, token_dir)):
            os.mkdir(os.path.join(working_dir, token_dir))

        if os.path.exists(os.path.join(working_dir, token_dir, pickle_file)):
            with open(os.path.join(working_dir, token_dir, pickle_file), 'rb') as token:
                cred = pickle.load(token)

        if not cred or not cred.valid:
            if cred and cred.expired and cred.refresh_token:
                cred.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
                cred = flow.run_local_server()

            with open(os.path.join(working_dir, token_dir, pickle_file), 'wb') as token:
                pickle.dump(cred, token)

        try:
            service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
            print(API_SERVICE_NAME, API_VERSION, 'service created successfully')
            return service
        except Exception as e:
            print(e)
            print(f'Failed to create service instance for {API_SERVICE_NAME}')
            os.remove(os.path.join(working_dir, token_dir, pickle_file))
            return None

    def get_emails(self, query_string):
        try:
            message_items, next_page_token = self.__search_gmail(query_string)

            while next_page_token:
                message_data, next_page_token = self.__search_gmail(query_string=query_string,
                                                                    pageToken=next_page_token)

                message_items.extend(message_data)

            return message_items
        except Exception as e:
            logging.error("Error to search emails in inbox", str(e))
            # raise NoEmailFound('No emails returned')

    def __search_gmail(self, query_string: str, pageToken=None):
        try:
            message_list_response = self.service.users().messages().list(
                userId='me',
                #labelIds=label_ids,
                q=query_string,
                pageToken=pageToken
            ).execute()
            logging.info(f"given the result based on __searching_gmail:{message_list_response}")
            message_items = message_list_response.get('messages')
            next_page_token = message_list_response.get('nextPageToken')
            return message_items, next_page_token
        except Exception as e:
            logging.error("Error to search gmail in inbox", str(e))

    def download_attachment(self, download_resume_folder, email_messages):
        try:
            if email_messages is None:
                return logging.warning(f"Query string not in valid format:{email_messages}")
            else:
                emailExtractor = EmailContentExtractor()
                for email_message in email_messages:
                    message_detail = emailExtractor.get_message_data(email_message['id'], self.service,
                                                                     msg_format='full',
                                                                     metadata_headers=['parts'])
                    message_detail_payload = message_detail.get('payload')
                    headers = message_detail_payload.get('headers')
                    if 'parts' in message_detail_payload:
                        for msgPayload in message_detail_payload['parts']:
                            file_name = msgPayload['filename']
                            print("This is the file name ", file_name)
                            body = msgPayload['body']
                            if 'attachmentId' in body:
                                attachment_id = body['attachmentId']
                                attachment_content = emailExtractor.get_file_detail(email_message['id'],
                                                                                    attachment_id,
                                                                                    file_name,
                                                                                    download_resume_folder,
                                                                                    self.service)
                                new_file_name = file_name
                                if os.path.exists(os.path.join(download_resume_folder, new_file_name)):
                                    # If it exists, create a new filename
                                    file_name, file_extension = os.path.splitext(file_name)
                                    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
                                    # Create a new filename with the current date and time appended
                                    new_file_name = f"{os.path.splitext(file_name)[0]}_{current_datetime}{file_extension}"

                                with open(os.path.join(download_resume_folder, new_file_name), 'wb') as _f:
                                    _f.write(attachment_content)
                                    _f.close()
                time.sleep(0.5)
                return 'Completed'
        except Exception as e:
            logging.error('Error occurs Query String is not proper format:- ', str(e))
