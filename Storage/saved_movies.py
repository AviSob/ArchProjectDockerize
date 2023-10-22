from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class SavedMovies(Base):
    __tablename__ = "saved_movies"

    movie_id = Column(String(150), nullable=False)
    trace_id = Column(String(20), nullable=False)
    notes = Column(String(150), nullable=False)
    save_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, nullable=False)
    season = Column(Integer, nullable=False)
    id = Column(Integer, primary_key=True)
    # timestamp = Column(String(100), nullable=False)
    date_created = Column(String(100), nullable=False)

    def __init__(self, movie_id, trace_id, notes, save_date, user_id, season):
        self.movie_id = movie_id
        self.trace_id = trace_id
        self.notes =  notes
        self.save_date = save_date
        self.user_id = user_id
        self.season =  season
        # self.timestamp = timestamp
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        dict = {}
        dict['movie_id'] = self.movie_id
        dict['trace_id'] = self.trace_id
        dict['notes'] = self.notes
        dict['save_date'] = self.save_date
        dict['user_id'] = self.user_id
        dict['season'] = self.season
        dict['id'] = self.id
        # dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created
        
        return dict