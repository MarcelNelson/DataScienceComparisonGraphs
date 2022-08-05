from sqlalchemy.orm import Session
from . import models

def get_salary(db:Session):
    return db.query(models.salary.player, models.salary.Position, models.salary.team).all()
