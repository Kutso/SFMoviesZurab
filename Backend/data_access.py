from database import db_session
from models import Location, Movie, MapLocationMovie


class Serializer:
    def serialize_location(self, address, fun_fact=None):
        if address is None:
            return None

        location_json = ({
            'id': address.id,
            'address': address.address,
            'lat': address.lat,
            'lng': address.lng,
        })
        if fun_fact is not None:
            location_json['funfact'] = fun_fact
        return location_json

    def serialize_movie(self, movie, fun_fact=None):
        if movie is None:
            return None

        actor_list = [
            movie.actor1.full_name,
            movie.actor2.full_name,
            movie.actor3.full_name
        ]
        actor_list = [x for x in actor_list if x is not None]

        movie_json = ({
            'id': movie.id,
            'title': movie.title,
            'poster_url': movie.poster_url,
            'imdb_rating': movie.imdb_rating,
            'release_year': movie.release_year,
            'writer': movie.writer.full_name,
            'director': movie.director.full_name,
            'actors': actor_list
        })

        if fun_fact is not None:
            movie_json['funfact'] = fun_fact

        return movie_json


class DbService:
    serializer = Serializer()

    def get_locations(self, movie_id=None):
        location_list = []

        if movie_id is None:
            query_list = Location.query.all()
            for address in query_list:
                location_list.append(self.serializer.
                                     serialize_location(address))
        else:
            query_list = db_session.query(Location, MapLocationMovie). \
                filter(MapLocationMovie.location_id == Location.id). \
                filter(MapLocationMovie.movie_id == movie_id).all()

            for list_item in query_list:
                address = list_item[0]
                funfact = list_item[1].fun_fact
                location_list.append(self.serializer.
                                     serialize_location(address, funfact))

        return location_list

    def get_location(self, location_id):
        location_item = Location.query. \
            filter(Location.id == location_id).first()
        location = self.serializer.serialize_location(location_item)
        return location

    def get_movies(self, location_id=None):
        movie_list = []

        if location_id is None:
            query_list = Movie.query.all()
            for movie in query_list:
                movie_list.append(self.serializer.serialize_movie(movie))
        else:
            query_list = db_session.query(Movie, MapLocationMovie). \
                filter(MapLocationMovie.movie_id == Movie.id). \
                filter(MapLocationMovie.location_id == location_id). \
                all()

            for list_item in query_list:
                movie_item = list_item[0]
                fun_fact = list_item[1].fun_fact
                movie_list.append(self.serializer.
                                  serialize_movie(movie_item, fun_fact))

        return movie_list

    def get_movie(self, movie_id):
        movie_item = Movie.query.filter(Movie.id == movie_id).first()
        movie = self.serializer.serialize_movie(movie_item)
        return movie

    def get_autocomplete_titles(self, prefix, count):
        if prefix == '':
            return []
        count = min(count, 10)
        query_list = Movie.query. \
            filter(Movie.title.ilike(prefix + '%')).limit(count)
        title_list = []
        for movie in query_list:
            title_list.append({
                'id': movie.id,
                'title': movie.title,
                'year': movie.release_year
            })

        return title_list

    def get_or_create(self, session, model, **kwargs):
        instance = session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            session.add(instance)
            session.commit()
            return instance

    def remove_session(self):
        db_session.remove()
