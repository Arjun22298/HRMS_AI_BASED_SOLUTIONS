import json
import logging
import os
from com.rb.hrms.resume_parser.utils.CreateAndMovedFolder import CreateFolder
from com.rb.hrms.resume_parser.daos.ResumeRawDataDAO import CilentResumeData


class AIResponseHandler:
    def __init__(self):
        self.list_of_json_data = []
        self.number_of_cv_failed = 0
        self.number_of_cv_processed = 0

    def handle_response(self, response, file,hrms_api_service):
        file_name = os.path.basename(file)
        self.response = response
        logging.info(self.response)
        self.clean_data = self.response.replace('```', "").replace('json', "").replace('JSON', "").replace('\n', '')
        logging.info(self.clean_data)
        data = json.loads(self.clean_data)
        if data.get('status') == 'Success':
            folder_path_data = CreateFolder()._move_file_to_destination_success(file)
            main_data = os.path.join(folder_path_data, file_name)
            data['processedDataFolder'] = main_data
        elif data.get('status') == 'Failed':
            failed_data = CreateFolder()._move_file_to_failed_destination(file)
            main_data = os.path.join(failed_data, file_name)
            data['processedDataFolder'] = main_data
        else:
            print(f"Unknown status for {file}: {data.get('status')}")
        if 'city' in data and data['city'] is not None:
            data['city'] = data['city'].upper()
        if 'higherQualification' in data and data['higherQualification'] is not None:
            data['higherQualification'] = data['higherQualification'].upper()

        CilentResumeData().insert_into_database(data,hrms_api_service=hrms_api_service)
        self.list_of_json_data.append(data)