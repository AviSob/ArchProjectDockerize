from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class MovieRating(Base):
    __tablename__ = "movie_ratings"

    id = Column(Integer, primary_key=True) 
    trace_id = Column(String(20), nullable=False)
    movie_id = Column(String(250), nullable=False)
    movie_name = Column(String(250), nullable=False)
    rating = Column(Integer, nullable=False)
    review = Column(String(350), nullable=False)
    # timestamp = Column (String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, movie_id, trace_id, movie_name, rating, review):
        self.movie_id = movie_id
        self.trace_id = trace_id
        self.movie_name = movie_name
        self.rating = rating
        self.review =  review
        # self.timestamp = timestamp
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        dict = {}
        dict['id'] = self.id
        dict['trace_id'] = self.trace_id
        dict['movie_id'] = self.movie_id
        dict['movie_name'] = self.movie_name
        dict['rating'] = self.rating
        dict['review'] = self.review
        # dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created

        return dict