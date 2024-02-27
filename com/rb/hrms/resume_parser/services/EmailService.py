from abc import ABC, abstractmethod

# Interface for Email Service Provider
class EmailService(ABC):

    @abstractmethod
    def process(self,request_data):
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def get_emails(self, folder):
        pass

    @abstractmethod
    def download_attachment(self, email_id, attachment_name):
        pass
