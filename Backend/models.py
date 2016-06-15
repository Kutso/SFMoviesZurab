from sqlalchemy import Column, Integer, Unicode, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    address = Column(Unicode(256), unique=True)
    lat = Column(Float)
    lng = Column(Float)

    def __init__(self, address, lat, lng):
        self.address = address
        self.lat = lat
        self.lng = lng

    def __repr__(self):
        return '<Location %r>' % self.address


class Celebrity(Base):
    __tablename__ = "celebrities"

    id = Column(Integer, primary_key=True)
    full_name = Column(Unicode(50), unique=True)

    def __init__(self, full_name):
        self.full_name = full_name

    def __repr__(self):
        return '<Celebrity %r>' % self.full_name


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(Unicode(100))
    poster_url = Column(Unicode(1024))
    imdb_rating = Column(Float)
    release_year = Column(Integer)

    writer_id = Column(Integer, ForeignKey('celebrities.id'))
    director_id = Column(Integer, ForeignKey('celebrities.id'))
    actor1_id = Column(Integer, ForeignKey('celebrities.id'))
    actor2_id = Column(Integer, ForeignKey('celebrities.id'))
    actor3_id = Column(Integer, ForeignKey('celebrities.id'))

    writer = relationship("Celebrity", foreign_keys='[Movie.writer_id]')
    director = relationship("Celebrity", foreign_keys='[Movie.director_id]')
    actor1 = relationship("Celebrity", foreign_keys='[Movie.actor1_id]')
    actor2 = relationship("Celebrity", foreign_keys='[Movie.actor2_id]')
    actor3 = relationship("Celebrity", foreign_keys='[Movie.actor3_id]')

    def __init__(self, title, poster_url, imdb_rating, release_year,
                 writer_id, director_id, actor1_id, actor2_id, actor3_id):
        self.title = title
        self.poster_url = poster_url
        self.imdb_rating = imdb_rating
        self.release_year = release_year
        self.writer_id = writer_id
        self.director_id = director_id
        self.actor1_id = actor1_id
        self.actor2_id = actor2_id
        self.actor3_id = actor3_id

    def __repr__(self):
        return '<Movie %r>' % self.title


class MapLocationMovie(Base):
    __tablename__ = 'map_location_movie'

    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.id'))
    movie_id = Column(Integer, ForeignKey('movies.id'))
    fun_fact = Column(Unicode(1024))

    location = relationship("Location")
    movie = relationship("Movie")

    def __init__(self, location_id, movie_id, fun_fact):
        self.location_id = location_id
        self.movie_id = movie_id
        self.fun_fact = fun_fact
