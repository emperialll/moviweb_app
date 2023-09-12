import requests
from flask import Blueprint, jsonify, request
from data_management.SQL_Data_Models import db, Movies, UserMovies, User

# OMDB API to get movie data
API: str = 'http://www.omdbapi.com/?apikey=6f0c3bf6&t='

api = Blueprint('api', __name__)


@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [user.to_dict() for user in users]
    return jsonify(user_list)


@api.route('/users/<user_id>/movies', methods=['GET'])
def user_favorite_movies(user_id):
    # Retrieve all movies associated with the user
    user_favorite_movies = db.session.query(UserMovies, Movies). \
        join(Movies, UserMovies.movie_id == Movies.movie_id). \
        filter(UserMovies.user_id == user_id).all()

    # Access the Movie object in the tuple
    movie_list = [movie[1].to_dict() for movie in user_favorite_movies]
    return jsonify(movie_list)


@api.route('/users/<user_id>/movies', methods=['POST'])
def add_movie_to_user(user_id):
    # Get the movie title from the request
    movie_title = request.json.get('movie_title')

    # Check if the movie exists in the Movies table
    existing_movie = Movies.query.filter_by(title=movie_title).first()

    if existing_movie:
        # Movie exists in the Movies table, add a new UserMovies row
        new_user_movie = UserMovies(
            user_id=user_id, movie_id=existing_movie.movie_id, note="")
        db.session.add(new_user_movie)
        db.session.commit()
    else:
        # Movie doesn't exist, fetch data from OMDB API
        omdb_url = API + movie_title
        response = requests.get(omdb_url)
        if response.status_code == 200:
            movie_dict_data = response.json()

            # Create a new Movie entry
            new_movie = Movies(
                title=movie_dict_data['Title'],
                year=movie_dict_data['Year'],
                rating=movie_dict_data['imdbRating'],
                genre=movie_dict_data['Genre'],
                director=movie_dict_data['Director'],
                writer=movie_dict_data['Writer'],
                actors=movie_dict_data['Actors'],
                plot=movie_dict_data['Plot'],
                language=movie_dict_data['Language'],
                country=movie_dict_data['Country'],
                poster=movie_dict_data['Poster'],
                _type=movie_dict_data['Type']
            )

            db.session.add(new_movie)
            db.session.commit()

            # Retrieve the movie_id after it's been added to the database
            movie_id = new_movie.movie_id  # Assuming 'id' is the primary key of the Movies table

            # Add a new UserMovies row
            new_user_movie = UserMovies(
                user_id=user_id, movie_id=movie_id, note="")
            db.session.add(new_user_movie)
            db.session.commit()

    return jsonify({"message": "Movie added successfully."})
