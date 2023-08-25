import requests
import json
from flask_sqlalchemy import SQLAlchemy
from data_management.SQL_Data_Models import db, User, Movies
from .DataManager import DataManagerInterface

# OMDB API to get movie data
API: str = 'http://www.omdbapi.com/?apikey=6f0c3bf6&t='


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, app, db_file_name):
        self.db = None  # Initialize the db attribute

        self.init_db(app, db_file_name)  # Call the init_db method

    def init_db(self, app, db_file_name):
        # Configure the database URI
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file_name}'

        # Initialize the SQLAlchemy extension with the Flask application
        db.init_app(app)

        self.db = db

    def get_all_users(self):
        # Fetch the list of users from the database
        users = User.query.all()
        return users

    def get_user_movies(self, user_id):
        pass

    def add_user(self, name, email, password):
        # Create a new User object with the form data
        new_user = User(name=name, email=email, password=password)

        # Add the user to the database
        self.db.session.add(new_user)
        self.db.session.commit()

    def add_movie(self, user_id, movie_title):
        response = requests.get(API + movie_title)
        response.raise_for_status()
        movie_dict_data = json.loads(response.text)
        if movie_dict_data['Response'] == 'False':
            return "Movie not found!"
        else:
            # Create a new movie object with the form data
            new_movie = Movies(user_id=user_id,
                               title=movie_dict_data['Title'],
                               director=movie_dict_data['Director'],
                               year=movie_dict_data['Year'],
                               rating=movie_dict_data['imdbRating'],
                               note="")

        # Add the user to the database
        db.session.add(new_movie)
        db.session.commit()

    def update_movie(self, user_id, movie_id, movie_title, movie_director,
                     movie_rating, movie_year, movie_note):
        pass

    def delete_movie(self, user_id, movie_id):
        pass
