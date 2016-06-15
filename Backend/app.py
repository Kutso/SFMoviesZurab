from flask import Flask, render_template, jsonify
from flask_cors import CORS
from data_access import DbService

app = Flask(__name__)
dbconnector = DbService()

CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/locations/')
@app.route('/api/locations/<int:location_id>/')
def get_location_data(location_id=None):
    if location_id is None:
        location_list = dbconnector.get_locations()
        return jsonify(location_list)
    else:
        location = dbconnector.get_location(location_id)
        movie_list = dbconnector.get_movies(location_id)
        return jsonify({
            'location_data': location,
            'movies': movie_list
        })


@app.route('/api/movies/autocomplete/')
@app.route('/api/movies/autocomplete/<string:prefix>/')
@app.route('/api/movies/autocomplete/<string:prefix>/<int:count>/')
def get_autocomplete_list(prefix='', count=5):
    title_list = dbconnector.get_autocomplete_titles(prefix, count)
    return jsonify(title_list)


@app.route('/api/movies/')
@app.route('/api/movies/<int:movie_id>/')
def get_movie_data(movie_id=None):
    if movie_id is None:
        movie_list = dbconnector.get_movies()
        return jsonify(movie_list)
    else:
        movie = dbconnector.get_movie(movie_id)
        location_list = dbconnector.get_locations(movie_id)

    return jsonify({
        'movie_data': movie,
        'locations': location_list
    })


@app.teardown_appcontext
def shutdown_session(exception=None):
    dbconnector.remove_session()


if __name__ == '__main__':
    app.run(debug=False)
