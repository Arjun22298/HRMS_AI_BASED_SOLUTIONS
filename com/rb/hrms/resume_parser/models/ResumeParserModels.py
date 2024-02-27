from sqlalchemy import Column, String, BigInteger, Text, ForeignKey, Boolean, TIMESTAMP, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import CreateSchema
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from com.rb.hrms.resume_parser.daos.DatabaseConnection import engine

Base = declarative_base()


class Candidate_Details_Hrms(Base):
    __tablename__ = 'candidate_details_hrms'
    id = Column(BigInteger, primary_key=True, index=True)
    candidate_id = Column(BigInteger,ForeignKey('candidate_data_details.id'))
    candidate_table =relationship('CandidateDetail')


class Status_Details(Base):
    __tablename__ = 'status'
    id = Column(BigInteger, primary_key=True, index=True)
    created_by = Column(String)
    created_date = Column(TIMESTAMP)
    last_modified_by = Column(String)
    last_modified_date = Column(TIMESTAMP)
    is_active = Column(Boolean, default=False)
    status_name = Column(String)
    status_type = Column(String)


class CandidateDetail(Base):
    __tablename__ = 'candidate_data_details'

    id = Column(BigInteger, primary_key=True, index=True)
    Candidate_Name = Column(String)
    Phone_Number = Column(String)
    Date_of_Birth = Column(String)
    Gender = Column(String)
    Current_Company_Name = Column(String)
    Previous_Company_Information = Column(Text)
    Email = Column(String)
    Total_Number_Of_Year_Experience = Column(String)
    Address = Column(Text)
    Linked_Url = Column(String)
    Certification = Column(Text)
    Skills = Column(Text)
    City = Column(String)
    Higher_Qualification = Column(String)
    Passing_Year = Column(String)
    Job_Role_And_Responsibilities = Column(String)
    Achievements = Column(String)
    Last_Company = Column(String)
    Status = Column(String)
    Processed_Data_Folder = Column(String)
    Clean_Status = Column(Boolean, default=False)
    Classification = Column(String)
    Cleaned_contact_no = Column(String)
    Cleaned_alt_contact_no = Column(String)
    Cleaned_city_id = Column(BigInteger, ForeignKey('city.id'))
    Cleaned_city = relationship('CityInfo')
    Cleaned_qualification_id = Column(BigInteger, ForeignKey('qualifications.id'))
    Cleaned_qualification = relationship('Qualification')
    json_data = Column(JSONB)
    process_date = Column(Date)


class CityInfo(Base):
    __tablename__ = 'city'
    id = Column(BigInteger, primary_key=True, index=True)
    city_name = Column(String)
    is_active = Column(Boolean, default=False)


class Qualification(Base):
    __tablename__ = 'qualifications'
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    is_active = Column(Boolean, default=False)


class JobDescription(Base):
    __tablename__ = 'job_description'
    id = Column(BigInteger, primary_key=True, index=True)
    job_title = Column(String)
    Json_data = Column(JSONB)
    Processed_date = Column(Date)
    File_Path = Column(String)


class CvVsJdCompritions(Base):
    __tablename__ = "JD_vs_CV_Comparison_details"
    id = Column(BigInteger, primary_key=True, index=True)
    position_id = Column(BigInteger, ForeignKey('job_description.id'))
    position_data = relationship('JobDescription')
    candidate_data_id = Column(BigInteger, ForeignKey('candidate_data_details.id'))
    candidate_data = relationship('CandidateDetail')
    compared_on = Column(Date)
    comparison_details = Column(JSONB)


Base.metadata.create_all(bind=engine)

"""def create_schnma(schemas: []):
    for schema in schemas:
        print("*****", schema)
        engine = create_engine(connection_string, echo=True, execution_options={"schema_translate_map": {None: schema}})
        with engine.connect() as conn:
            try:
                if engine.dialect.has_schema(conn, schema):
                    Base.metadata.create_all(conn)
                else:
                    conn.execute(CreateSchema(schema))
                    Base.metadata.create_all(conn)
                conn.commit()
            except Exception as e:
                print(f"Error creating schema {schema}: {str(e)}")
                conn.rollback()"""

"""x = create_schnma(['public'])"""
