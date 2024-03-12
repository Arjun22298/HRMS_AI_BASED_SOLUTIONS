from com.rb.hrms.resume_parser.logging.RollingFileLogger import RollingFileLogger
import logging


class BaseHRMS:

    def __init__(self):
        self.logger = RollingFileLogger("D:/ResumeParserProject/logs/ResumeParser.log")


# Example usage:
if __name__ == "__main__":
    obj = BaseHRMS()
    obj.logger.log("This is an info message", level=logging.INFO)
    obj.logger.log("This is a warning message", level=logging.WARNING)
    obj.logger.log("This is an error message", level=logging.ERROR)
    obj.logger.log("This is a critical message", level=logging.CRITICAL)
