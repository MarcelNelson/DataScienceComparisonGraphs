from sqlalchemy import Column, Float, String, Integer, Numeric
from .database import Base

class datascience(Base):
    __tablename__ = "datascience"
    id = Column(Integer, primary_key=True, index=True)
    work_year = Column(String)
    experience_level = Column(String)
    employment_type = Column(String)
    job_title= Column(String)
    salary= Column(Numeric)
    salary_currency= Column(String)
    salary_usd= Column(Numeric)
    employee_residence= Column(String)
    remote_work_percent= Column(Numeric)
    company_location= Column(String)
    company_size= Column(String)
