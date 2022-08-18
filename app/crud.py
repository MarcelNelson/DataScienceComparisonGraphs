from sqlalchemy.orm import Session
from . import models

def get_datascience(db:Session):
    return db.query(models.datascience.work_year, models.datascience.experience_level, models.datascience.employment_type, models.datascience.job_title, models.datascience.salary, models.datascience.salary_currency, models.datascience.salary_usd, models.datascience.employee_residence, models.datascience.remote_work_percent, models.datascience.company_location, models.datascience.company_size).all()
