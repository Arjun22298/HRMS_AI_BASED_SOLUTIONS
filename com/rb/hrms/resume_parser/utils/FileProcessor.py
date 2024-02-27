import glob
import docx2txt
import logging
import os
from pdfminer.high_level import extract_text
class FileProcessor:
    def __init__(self):
        self.msg_list = []

    def pdf(self, file):
        data = extract_text(file)
        return data

    def word(self, file):
        try:
            data = docx2txt.process(file)
            return data
        except Exception as e:
            logging.error("Error to get data from Word format resume", str(e))

    """def __convert_doc_to_docx(self,file_path):
        try:
            self.list_of_files = glob.glob(file_path)
            for file_path in self.list_of_files:
                normalized_path = os.path.normpath(file_path)
                # Create a new filename for the converted file
                new_file_path = os.path.splitext(normalized_path)[0] + ".docx"

                # Create an instance of the Word application
                word_app = win32.Dispatch("Word.Application")

                # Open the .doc file
                doc = word_app.Documents.Open(normalized_path)

                # Save the .doc file as .docx
                doc.SaveAs2(new_file_path, FileFormat=16)

                # Close the .doc file
                doc.Close()

                # Quit the Word application
                word_app.Quit()

                # remove doc file from folder
                os.remove(normalized_path)
                return new_file_path
        except Exception as e:
            logging.error("Error to convert doc file into docx", str(e))"""
