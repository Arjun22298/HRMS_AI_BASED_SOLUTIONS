from com.rb.hrms.resume_parser.utils.AIResponseHandler import AIResponseHandler
import logging


class ResumeParsingStatus(AIResponseHandler):

    def process_cv(self):
        try:
            for cv_data in self.list_of_json_data:
                if cv_data['status'] == 'Success':
                    self.number_of_cv_processed += 1
                elif cv_data['status'] == 'Failed':
                    self.number_of_cv_failed += 1
        except Exception as e:
            logging.warning("Exception will occur on Resume Parser Data ", str(e))
        processing_extraction_success_pdf = {
            'Process': 'CV Processing from mailbox',
            'Status': 'Success',
            'CVs processed': self.number_of_cv_processed
        }

        processing_extraction_failed_pdf = {
            'Process': 'Cv Processing for mailbox',
            'Status': 'Failed',
            'CVs processed': self.number_of_cv_failed
        }
        return processing_extraction_success_pdf, processing_extraction_failed_pdf
