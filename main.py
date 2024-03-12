from fastapi import FastAPI
from uvicorn import run
from com.rb.hrms.resume_parser.router import resume_attachments_download_router
from com.rb.hrms.resume_parser.router import cleanResumeDataRouter
from com.rb.hrms.resume_parser.router import parseJDRouter
from com.rb.hrms.resume_parser.router import parseSingleResumeRouter
from com.rb.hrms.resume_parser.router import ResumeParsingProcessorRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(resume_attachments_download_router.router)
app.include_router(cleanResumeDataRouter.router)
app.include_router(parseJDRouter.router)
app.include_router(parseSingleResumeRouter.router)
app.include_router(ResumeParsingProcessorRouter.router)

if __name__ == "__main__":
    run(app, host=str("192.168.1.106"), port=int(7000))
