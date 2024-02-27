import os
import json
from com.rb.hrms.resume_parser.services.EmailService import EmailService
class OutlookService(EmailService):
    def __init__(self, config_file_path='outlook_config.json'):
        self.config_file_path = config_file_path
        self.account = None

    def load_credentials(self):
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'r') as file:
                config_data = json.load(file)
                client_id = config_data['client_id']
                client_secret = config_data['client_secret']
                token_backend = FileSystemTokenBackend(token_path=config_data['token_path'])
                self.account = Account((client_id, client_secret), token_backend=token_backend)
        else:
            raise ValueError("Config file not found.")

    def authenticate(self):
        if not self.account.is_authenticated:
            self.account.authenticate(scopes=['basic', 'message_all', 'message_all_extended'])
            self.account.get_access_token()
            self.account.save_token()

    def connect(self):
        self.load_credentials()
        self.authenticate()

    def get_emails(self, folder):
        mailbox = self.account.mailbox()
        folder = mailbox.get_folder(folder)
        messages = folder.get_messages()
        return messages

    def download_attachment(self, email_id, attachment_name):
        message = Message(account=self.account, folder='inbox', id=email_id)
        attachments = message.attachments

        for attachment in attachments:
            if attachment.filename == attachment_name:
                with open(attachment_name, 'wb') as f:
                    f.write(attachment.content)

    def move_to_folder(self, email_id, folder):
        message = Message(account=self.account, folder='inbox', id=email_id)
        message.move(folder)
