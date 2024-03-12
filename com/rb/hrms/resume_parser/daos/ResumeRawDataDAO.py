import json
import logging
import pandas as pd
from datetime import datetime
import requests
from com.rb.hrms.resume_parser.constants.HRMSApiConstants import *

from com.rb.hrms.resume_parser.logging.Logging_file import custom_logger

logger = custom_logger


class CilentResumeData:
    @custom_logger.log_around
    def insert_into_database(self, list_of_json_data, hrms_api_service):
        try:
            # insert_into_database = CandidateDataRawDetails()

            dataframe = pd.DataFrame([list_of_json_data])
            dataframe['higherQualification'] = dataframe['higherQualification'].apply(
                lambda x: x.split('/')[0].strip() if x else None)
            json_columns = ['previousCompanyInformation', 'skills']
            for column in json_columns:
                dataframe[column] = dataframe[column].apply(json.dumps)
            dataframe['jsonData'] = dataframe.apply(
                lambda row: json.dumps({k: v for k, v in row.to_dict().items() if v is not None}),
                axis=1
            )
            current_time = datetime.now()
            date = dataframe['processDate'] = current_time.strftime('%Y-%m-%dT%H:%M:%S')
            logging.info(date)
            json_data = dataframe.to_json(orient='records')
            json_data = json.loads(json_data)
            formatted_json = json.dumps(json_data[0], indent=4)
            self.insert_raw_data_into_database(hrms_api_service=hrms_api_service, data=formatted_json)
            # logging.info("Data inserted into the database.")
        except Exception as e:
            logging.error(f"Error inserting data into the database: {e}")

    @custom_logger.log_around
    def insert_raw_data_into_database(self, hrms_api_service, data):
        try:
            url = f"{hrms_api_service.base_url}/{INSERT_CANDIDATE_RAW_DATA_INTO_DATABASE}"
            response = self.hrms_api_call_to_insert_raw_data(headers=hrms_api_service.headers, method='POST',
                                                             url=url,
                                                             data=data)
        except Exception as e:
            logging.error(str(e), exc_info=True)

    @custom_logger.log_around
    def hrms_api_call_to_insert_raw_data(self, headers, method, url, data=None):
        try:
            response = requests.request(headers=headers, method=method, data=data, url=url)
            response.raise_for_status()
            print(response.json())
            if response:
                print(f"API Call to {url} | Method: {method} | Status Code: {response.status_code}")
                return response.json() if 'application/json' in response.headers.get('Content-Type',
                                                                                     '') else response.text
            else:
                print(f"API Call to {url} | Method: {method} | Failed. No response received.")
        except requests.exceptions.HTTPError as errh:
            print("HTTP Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Oops: Something Else", err)

    """"def _data_of_candidate_tables(self):
        try:
            candidate_tables = self._session.query(CandidateDetail.id).all()
            for candidate_id in candidate_tables:
                candidate_id_data = candidate_id.id
                self._insert_into_hrms_database(candidate_id_data)
        except Exception as e:
            logging.warning("warning Candidate_id not add on HRMS Tables", str(e))

    def _insert_into_hrms_database(self, candidate_id):
        try:
            candidate_data = self._session.query(Candidate_Details_Hrms).filter_by(candidate_id=candidate_id).first()
            if candidate_data:
                logging.info(f"HRMS entry for Candidate ID {candidate_id} already exists. Skipping.")
            else:
                new_candidate_id = Candidate_Details_Hrms(candidate_id=candidate_id)
                self._session.add(new_candidate_id)
                logging.info(f"HRMS entry added for Candidate ID: {candidate_id}")
            self._session.commit()
            # self._session.flush()
        except Exception as e:
            logging.error(f"Error inserting data into the HRMS table: {e}")
            # Rollback the session in case of an error
            self._session.rollback()
            raise
        finally:
            return None

    @staticmethod
    def read_dataframe_from_database(ml_skills, table_name='candidate_data_details'):
        try:
            # Read data from the specified table into a Pandas DataFrame
            query = f'SELECT * FROM {table_name}'
            dataframe = pd.read_sql(query, con=engine)
            ml_candidates = dataframe[dataframe['Skills'].str.contains('|'.join(ml_skills), case=False, na=False)]

            # Select specific columns
            data = ml_candidates[
                ['Candidate_Name', 'Email', 'Higher_Qualification', 'City', 'Total_Number_Of_Years_Experience',
                 'Previous_Company_Information', 'Processed_Data_Folder']]
        except Exception as e:
            logging.error(f"Error reading data from the database: {e}")"""
