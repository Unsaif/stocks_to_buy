from sqlalchemy.orm import Session

from .import models, schemas

def get_trades(db: Session):
    return db.query(models.Trade).all()