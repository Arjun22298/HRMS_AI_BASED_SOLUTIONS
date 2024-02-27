from com.rb.hrms.resume_parser.utils.ResumeProcessor import ResumeProcessor


class ResumeParserWithAIService:
    def __init__(self):
        self.resume_processor = ResumeProcessor()

    def process_resumes(self, folder_path):
        response_ai_resume_parser = self.resume_processor.process(folder_path)
        return response_ai_resume_parser
