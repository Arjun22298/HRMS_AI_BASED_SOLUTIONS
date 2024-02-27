import logging
from logging.handlers import RotatingFileHandler


class RollingFileLogger:
    def __init__(self, log_file, max_bytes=1048576, backup_count=5):
        self.log_file = log_file
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.logger = self._get_logger()

    def _get_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('[%(asctime)s] - [PID: %(process)d] - [%(levelname)s] - %(message)s')

        file_handler = RotatingFileHandler(
            filename=self.log_file,
            maxBytes=self.max_bytes,
            backupCount=self.backup_count
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger

    def log(self, message, level=logging.INFO):
        if level == logging.DEBUG:
            self.logger.debug(message)
        elif level == logging.INFO:
            self.logger.info(message)
        elif level == logging.WARNING:
            self.logger.warning(message)
        elif level == logging.ERROR:
            self.logger.error(message)
        elif level == logging.CRITICAL:
            self.logger.critical(message)
        else:
            raise ValueError("Invalid log level")