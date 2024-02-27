import os
import shutil
import logging
from datetime import date


class CreateFolder:
    def __init__(self):
        logging.basicConfig(filename='file_mover.log', level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def _move_file_to_destination_success(self, file):
        today = date.today()
        destination_folder_success = os.path.abspath(os.path.join('../../../../Success', today.strftime('%Y-%m-%d')))
        destination_file_path = os.path.join(destination_folder_success, os.path.basename(file))

        if os.path.exists(destination_file_path):
            logging.info(f"File {file} already exists at {destination_folder_success}. Overwriting the file.")
            try:
                os.remove(destination_file_path)
            except Exception as e:
                logging.error(f"Error deleting existing file {destination_file_path}: {e}")

        logging.info(f"Moving file {file} to {destination_folder_success}")
        try:
            os.makedirs(destination_folder_success, exist_ok=True)
            shutil.move(file, destination_folder_success)
            logging.info(f"File {file} moved successfully to {destination_folder_success}")
            return destination_folder_success
        except Exception as e:
            logging.error(f"Error moving file {file}: {e}")

    def _move_file_to_failed_destination(self, file):
        today = date.today()
        destination_folder_failed = os.path.abspath(os.path.join('../../../../Failed', today.strftime('%Y-%m-%d')))
        destination_file_path = os.path.join(destination_folder_failed, os.path.basename(file))
        if os.path.exists(destination_file_path):
            logging.info(f"File {file} already exists at {destination_folder_failed}. Overwriting the file.")
            try:
                os.remove(destination_file_path)  # Delete existing file
            except Exception as e:
                logging.error(f"Error deleting existing file {destination_file_path}: {e}")

        logging.info(f"Moving file {file} to {destination_folder_failed}")
        try:
            os.makedirs(destination_folder_failed, exist_ok=True)
            shutil.move(file, destination_folder_failed)
            logging.info(f"File {file} moved successfully to {destination_folder_failed}")
            return destination_folder_failed
        except Exception as e:
            logging.error(f"Error moving file {file}: {e}")
