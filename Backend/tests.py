import unittest
from database import db_session
from models import Location, Movie, Celebrity
from data_access import Serializer, DbService
from data_init import DataCollector
import json
import urllib2


class TestSerializators(unittest.TestCase):
    serializer = Serializer()

    def test_serialize_movie(self):
        movie_item = Movie.query.filter(Movie.id == 1).first()
        movie = self.serializer.serialize_movie(movie_item)
        self.assertEqual('id' in movie, True)
        self.assertEqual('title' in movie, True)
        self.assertEqual('poster_url' in movie, True)
        self.assertEqual('imdb_rating' in movie, True)
        self.assertEqual('release_year' in movie, True)
        self.assertEqual('writer' in movie, True)
        self.assertEqual('director' in movie, True)
        self.assertEqual('actors' in movie, True)
        movie = self.serializer.serialize_movie(movie_item, "fact")
        self.assertEqual('funfact' in movie, True)

    def test_serialize_location(self):
        location_item = Location.query.filter(Location.id == 1).first()
        location = self.serializer.serialize_location(location_item)
        self.assertEqual('id' in location, True)
        self.assertEqual('address' in location, True)
        self.assertEqual('lat' in location, True)
        self.assertEqual('lng' in location, True)
        self.assertEqual('funfact' in location, False)
        location = self.serializer.serialize_location(location_item, "fact")
        self.assertEqual('funfact' in location, True)


class TestDataAccess(unittest.TestCase):
    dbconnector = DbService()

    def test_get_all_locations(self):
        locations = self.dbconnector.get_locations()
        self.assertNotEqual(locations, None)
        self.assertEqual(len(locations) > 0, True)

    def test_get_location_for_movie(self):
        locations = self.dbconnector.get_locations(1)
        self.assertNotEqual(locations, None)
        self.assertEqual(len(locations) > 0, True)

    def test_get_location(self):
        location = self.dbconnector.get_location(1)
        self.assertNotEqual(location, None)
        self.assertEqual(location["id"], 1)

        location = self.dbconnector.get_location(-1)
        self.assertEqual(location, None)

    def test_get_all_movie(self):
        movies = self.dbconnector.get_movies()
        self.assertNotEqual(movies, None)
        self.assertEqual(len(movies) > 0, True)

    def test_get_movie_for_location(self):
        movies = self.dbconnector.get_movies(1)
        self.assertNotEqual(movies, None)
        self.assertEqual(len(movies) > 0, True)

    def test_get_movie(self):
        movie = self.dbconnector.get_movie(1)
        self.assertNotEqual(movie, None)
        self.assertEqual(movie["id"], 1)
        movie = self.dbconnector.get_movie(-1)
        self.assertEqual(movie, None)

    def test_autocomplete(self):
        title_list = self.dbconnector.get_autocomplete_titles(u'zzz', 5)
        self.assertEqual(len(title_list), 0)
        self.assertNotEqual(title_list, None)

        title_list = self.dbconnector.get_autocomplete_titles(u'a', 20)
        self.assertEqual(len(title_list) > 10, False)

        title_list = self.dbconnector.get_autocomplete_titles(u'B', 1)
        self.assertEqual(len(title_list) == 1, True)
        self.assertEqual(title_list[0]['title'].lower()[0], u'b')

    def test_get_or_create(self):
        writer = self.dbconnector.get_or_create(db_session,
                                                Celebrity,
                                                full_name=u'Joan Cusack')
        self.assertNotEqual(writer, None)
        self.assertEqual(writer.full_name, u'Joan Cusack')


class TestDataInitialization(unittest.TestCase):
    collector = DataCollector();

    def test_get_coordinates(self):
        address = 'Golden Gate Park'
        coordinates = self.collector.get_coordinates(address)
        self.assertNotEqual(coordinates, None)
        self.assertEqual(coordinates[0], 37.76904)
        self.assertEqual(coordinates[1], -122.4835193)

    def test_get_movie_info(self):
        title = 'The Matrix'
        year = 1999
        movie_info = self.collector.get_movie_info(title, year)
        self.assertNotEqual(movie_info, None)

        # if matrix falls below 8.5, then something's fishy
        self.assertEqual(movie_info[1] >= 8.5, True)
        self.assertNotEqual(movie_info[0], None)

    def test_get_location_id(self):
        address = u'Epic Roasthouse (399 Embarcadero)'
        location_id = self.collector.get_location_id(address)

        self.assertNotEqual(location_id, None)
        self.assertEqual(location_id, 1)

    def test_data_source_valid(self):
        data = json.load(urllib2.
                         urlopen("https://data.sfgov.org/resource/wwmu-gmzc.json"))

        self.assertNotEqual(data, None)
        self.assertEqual(data.count > 0, True)


if __name__ == '__main__':
    unittest.main()
