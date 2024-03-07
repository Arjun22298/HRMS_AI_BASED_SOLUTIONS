from com.rb.hrms.resume_parser.utils.ResumeProcessor import ResumeProcessor


class ResumeParserWithAIService:
    def __init__(self, Authorization, X_TenantID):
        self.resume_processor = ResumeProcessor(Authorization, X_TenantID)

    def process_resumes(self, folder_path):
        response_ai_resume_parser = self.resume_processor.process(folder_path)
        return response_ai_resume_parser

    def process_single_resume(self, folder_path):
        response_single_resume = self.resume_processor.process(folder_path)
        return response_single_resume

