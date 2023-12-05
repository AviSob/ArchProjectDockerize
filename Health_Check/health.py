from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class Health(Base):
    __tablename__ = "health"

    log_id = Column(Integer, primary_key=True) 
    service = Column(String(250), nullable=False)
    status = Column(String(250), nullable=False)
    time_stamp = Column(String(250), nullable=False)

    def __init__(self, service, status, time_stamp):
        self.service = service
        self.status = status
        self.time_stamp = time_stamp

    def to_dict(self):
        dict = {}
        dict['log_id'] = self.log_id
        dict['service'] = self.service
        dict['status'] = self.status
        dict['time_stamp'] = self.time_stamp


        return dict