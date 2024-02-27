import glob
import os
import logging
from com.rb.hrms.resume_parser.utils.FileProcessor import FileProcessor
from com.rb.hrms.resume_parser.utils.JDResponseHandler import JDResponseHandler


class JDProcessor:

    def parsed_JD(self, folder_path):
        try:
            list_of_files = glob.glob(f'{folder_path}\\*.*')
            for file in list_of_files:
                file_extension = os.path.splitext(file)[-1].lower()
                if file_extension == '.pdf':
                    data = FileProcessor().pdf(file)
                elif file_extension == '.docx' or file_extension == '.doc':
                    data = FileProcessor().word(file)
                else:
                    logging.warning(f"Unsupported file format: {file_extension}")
                    continue
                # TODO - -- > AI WILL PARSED THE JD AND GIVEN ME ACCURATE FORMAT ..
                try:
                    Response = self.generate_content_with_retry(f"{data},{job_description_details}")
                    extract_jb_data = Response.text
                    handling_response_of_jd_parser = JDResponseHandler()
                    handling_response_of_jd_parser._handling_jd_ai_response(extract_jb_data, file)
                except Exception as e:
                    logging.warning(f'Exception comes from Parsed based on JD {str(e)}')

        except Exception as e:
            print("Exception error comes", str(e))
