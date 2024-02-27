import json
import os
from datetime import datetime
import shutil
import logging



class JDResponseHandler:

    def _handling_jd_ai_response(self, response, file):
        try:
            file_name = os.path.basename(file)
            self.response = response
            self.clean_data = self.response.replace('```', "").replace('json', "").replace('JSON', "").replace('\n', '')
            json_data = json.loads(self.clean_data)
            if json_data.get('job_title') is not None:
                job_title = json_data['job_title'].upper()
                processed_date = datetime.now().date()
                destination_folder_path = os.path.abspath(DESTINATION_JD_FOLDER_PATH)
                #TODO --> DESTINATION JD FOLDER PATH ...
                print(destination_folder_path)
                file_directory_name = os.path.join(destination_folder_path, file_name)
                if os.path.exists(file_directory_name):
                    os.remove(file_directory_name)
                shutil.move(file, DESTINATION_JD_FILE_PATH)
                # TODO ---> DESTINATION JD FOLDER PATH ...
                return {'job_title': job_title, 'json_data': json_data, 'processed_date_of_jd': processed_date,
                        'file_directory': file_directory_name}
        except Exception as e:
            logging.error(f"Exception occurred handling AI response for job description: {str(e)}")
