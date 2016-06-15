import json
import urllib2
from database import db_session
from models import Location, Movie, Celebrity, MapLocationMovie
from database import init_db
from data_access import DbService

dbconnector = DbService()


class DataCollector:
    def get_coordinates(self, address):
        address = address.encode('utf-8')
        address = 'San Francisco ' + address
        url = 'http://maps.googleapis.com/maps/api/geocode/json?address=' \
              + urllib2.quote(address)
        response = json.load(urllib2.urlopen(url))
        if response['results']:
            location = response['results'][0]['geometry']['location']
            latitude, longitude = location['lat'], location['lng']
        else:
            latitude, longitude = None, None
        return latitude, longitude

    def get_movie_info(self, title, year):
        title = title.encode('utf-8')
        url = 'http://omdbapi.com/?t=' + urllib2.quote(title) \
              + '&y=' + str(year) + 'plot=short&r=json'
        response = json.load(urllib2.urlopen(url))
        if response['Response'] == "True":
            poster_url = response['Poster']
            imdb_rating = (response['imdbRating']
                           if response['imdbRating'] != 'N/A' else None)
        else:
            poster_url, imdb_rating = None, None
        return poster_url, imdb_rating

    def get_location_id(self, address):
        location_instance = db_session.query(Location). \
            filter_by(address=address).first()
        if location_instance:
            return location_instance.id

        coordinates = self.get_coordinates(address)
        lat = coordinates[0]
        lng = coordinates[1]
        location = dbconnector.get_or_create(db_session,
                                             Location, address=address,
                                             lat=lat, lng=lng)
        return location.id

    def get_movie_id(self, pin_data):
        title = pin_data['title'].strip()
        year = (int(pin_data['release_year'].strip())
                if pin_data.has_key('release_year') else None)

        writer = (pin_data['writer'].strip()
                  if pin_data.has_key('writer') else None)

        director = (pin_data['director'].strip()
                    if pin_data.has_key('director') else None)

        actor1 = (pin_data['actor_1'].strip()
                  if pin_data.has_key('actor_1') else None)

        actor2 = (pin_data['actor_2'].strip()
                  if pin_data.has_key('actor_2') else None)

        actor3 = (pin_data['actor_3'].strip()
                  if pin_data.has_key('actor_3') else None)

        movie_instance = db_session.query(Movie) \
            .filter_by(title=title,
                       release_year=year).first()
        if movie_instance:
            return movie_instance.id

        movie_info = self.get_movie_info(title, year)
        writer_id = dbconnector.get_or_create(db_session,
                                              Celebrity,
                                              full_name=writer).id

        director_id = dbconnector.get_or_create(db_session,
                                                Celebrity,
                                                full_name=director).id

        actor1_id = dbconnector.get_or_create(db_session,
                                              Celebrity,
                                              full_name=actor1).id

        actor2_id = dbconnector.get_or_create(db_session,
                                              Celebrity,
                                              full_name=actor2).id

        actor3_id = dbconnector.get_or_create(db_session,
                                              Celebrity,
                                              full_name=actor3).id

        movie = dbconnector.get_or_create(db_session, Movie, title=title,
                                          release_year=year,
                                          poster_url=movie_info[0],
                                          imdb_rating=movie_info[1],
                                          writer_id=writer_id,
                                          director_id=director_id,
                                          actor1_id=actor1_id,
                                          actor2_id=actor2_id,
                                          actor3_id=actor3_id)
        return movie.id


def main():
    init_db()
    data = json.load(urllib2.
                     urlopen("https://data.sfgov.org/resource/wwmu-gmzc.json"))

    collector = DataCollector()
    for pin_data in data:
        if pin_data.has_key('locations') and pin_data.has_key('title'):
            location_id = collector. \
                get_location_id(pin_data['locations'].strip())

            movie_id = collector.get_movie_id(pin_data)

            if pin_data.has_key('fun_facts'):
                fun_fact = pin_data['fun_facts'].strip()
            else:
                fun_fact = None

            mapped = dbconnector.get_or_create(db_session, MapLocationMovie,
                                               location_id=location_id,
                                               movie_id=movie_id,
                                               fun_fact=fun_fact)


if __name__ == "__main__":
    main()
