from datetime import datetime, timedelta
from com.rb.hrms.resume_parser.logging.RollingFileLogger import RollingFileLogger
import logging


class QueryBuilder():

    def __init__(self):
        self.logger = RollingFileLogger("D:/ResumeParserProject/logs/ResumeParser.log")

    def parse_label_with_prefix(self,input_string):
        self.logger.log("Entry in method QueryBuilder().parse_label_with_prefix()", level=logging.INFO)
        # Split the string by ","
        tokens = input_string.split(',')

        # Append "label:" as a prefix to each token separated by " OR "
        labeled_tokens = [f'label:{token.strip()}' for token in tokens]

        # Join the labeled tokens with " OR " to form the final string
        result_string = ' OR '.join(labeled_tokens)
        self.logger.log("Exiting from  method QueryBuilder().parse_label_with_prefix()", level=logging.INFO)
        return result_string

    def parse_subject_with_prefix(self,input_string):
        # Split the string by ","
        tokens = input_string.split(',')

        # Append "label:" as a prefix to each token separated by " OR "
        labeled_tokens = [f'{token.strip()}' for token in tokens]

        # Join the labeled tokens with " OR " to form the final string
        result_string = ' OR '.join(labeled_tokens)
        return result_string

    def __parse_dates(self, date_string, is_specific_processing):
        date_values = date_string.split(',')
        after_date = datetime.strptime(date_values[0].strip(), "%Y/%m/%d").date()
        processing_flag = False
        if is_specific_processing.lower() == "false":
            processing_flag = False
        else:
            processing_flag = True

        if processing_flag:
            # Check if there is a second date value before assigning it to 'before'
            if len(date_values) > 1:
                before_date = datetime.strptime(date_values[1].strip(), "%Y/%m/%d").date()
            else:
                before_date = self.get_date_based_today(False, processing_flag, after_date)
        else:
            after_date = self.get_date_based_today(True, processing_flag, None)
            before_date = datetime.now().date()

        date_string = f"after:{after_date.strftime('%Y-%m-%d')} before:{before_date.strftime('%Y-%m-%d')}"
        print("This is the time ",date_string)
        return date_string


    def get_date_based_today(self, is_yesterday, is_specific_processing, after_date):
        # Get today's date
        today = datetime.now().date()

        # Calculate yesterday's date
        if (is_yesterday):
            process_date = today - timedelta(days=1)
        else:
            if is_specific_processing:
                process_date = after_date + timedelta(days=1)
            else:
                process_date = today + timedelta(days=1)
        return process_date

    def build_query(self,request_data):
        """ This build query build the Query to Search Email and Download the attachments ...!"""
        date_string = request_data.email_specific_date
        date_query = self.__parse_dates(date_string,request_data.email_specific_date_flag)

        print(f"After date: {date_query}")
        inbox_string = request_data.email_folders_to_scan
        folder_query = self.parse_label_with_prefix(inbox_string)
        print(folder_query)

        search_tokens = request_data.search_query_tokens
        subject_query = self.parse_subject_with_prefix(search_tokens)
        print(subject_query)

        attachment_query = 'has:attachment'
        filename_query = 'filename:pdf OR filename:doc OR filename:docx'
        final_query_string = f"({folder_query}) {date_query} {attachment_query} {filename_query} ({subject_query})"
        print(f"Final Query String :: {final_query_string}")
        return final_query_string

#final_query_string = QueryBuilder().build_query()
#print(f"Final Query String :: {final_query_string}")