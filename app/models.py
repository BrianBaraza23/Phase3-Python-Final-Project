from sqlalchemy import ForeignKey, Column, Integer, String, Float
from sqlalchemy.orm import relationship
from database import Base


class Actor(Base):
    __tablename__ = 'actors'

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    movies = relationship('Movie', backref='actor')

    def __repr__(self):
        return f"Actor(id={self.id}, " +\
                f"name={self.name})"


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer(), primary_key=True)
    title = Column(String())
    rating = Column(Float())
    category = Column(Integer())

    actor_id = Column(Integer(), ForeignKey('actors.id'))

    def __repr__(self):
        return f"Movie(id={self.id},  " +\
                f"title={self.title}, " +\
                f"category={self.category}, " +\
                f"rating={self.rating}, "+\
                f"actor_id={self.actor_id})"