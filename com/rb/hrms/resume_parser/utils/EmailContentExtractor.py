import base64
import logging
from typing import List

class EmailContentExtractor():
    def get_file_detail(self, message_id, attachment_id, file_name, save_location,service):
        try:
            response = service.users().messages().attachments().get(
                userId='me',
                messageId=message_id,
                id=attachment_id
            ).execute()
            file_data = base64.urlsafe_b64decode(response.get('data').encode('UTF-8'))
            return file_data
        except Exception as e:
            logging.error("Error to get file details", str(e))

    def get_message_data(self, message_id, service, msg_format='metadata', metadata_headers: List = None):
        try:
            message_detail = service.users().messages().get(
                userId='me',
                id=message_id,
                format=msg_format,
                metadataHeaders=metadata_headers
            ).execute()
            return message_detail
        except Exception as e:
            logging.error("Error to get message data from email service", str(e))